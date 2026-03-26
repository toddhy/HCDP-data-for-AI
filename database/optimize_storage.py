import os
import shutil
import tiledb
import numpy as np
import json
import time

def optimize_array(array_uri):
    if not tiledb.array_exists(array_uri):
        print(f"Array {array_uri} does not exist.")
        return

    backup_base = array_uri + "_backup"
    backup_uri = backup_base + "_" + str(int(time.time()))
    
    # Use system temp directory for better isolation from file watchers on Windows
    import tempfile
    temp_parent = tempfile.gettempdir()
    temp_uri = os.path.join(temp_parent, os.path.basename(array_uri) + "_compressed_" + str(int(time.time())))
    
    print(f"\n--- Optimizing array: {array_uri} ---")
    print(f"Building compressed version in temp: {temp_uri}")
    
    with tiledb.DenseArray(array_uri, mode='r') as src_array:
        schema = src_array.schema
        meta = dict(src_array.meta)
        
        # Check if already compressed
        filters = schema.attr(0).filters
        if any(isinstance(f, tiledb.ZstdFilter) for f in filters):
            print(f"Array {array_uri} already has Zstd compression. Skipping optimization.")
            return

        # Create new schema with compression
        dom = schema.domain
        new_attr = tiledb.Attr(
            name=schema.attr(0).name,
            dtype=schema.attr(0).dtype,
            fill=schema.attr(0).fill,
            filters=tiledb.FilterList([tiledb.ZstdFilter(level=7)])
        )
        
        new_schema = tiledb.ArraySchema(
            domain=dom,
            sparse=schema.sparse,
            attrs=[new_attr],
            cell_order=schema.cell_order,
            tile_order=schema.tile_order
        )
        
        print(f"Creating compressed array at {temp_uri}...")
        tiledb.DenseArray.create(temp_uri, new_schema)
        
        # Copy metadata
        with tiledb.DenseArray(temp_uri, mode='w') as dest_array:
            for key, value in meta.items():
                dest_array.meta[key] = value

        # Copy data in chunks
        time_mapping = json.loads(meta.get("time_mapping", "{}"))
        num_slices = meta.get("next_time_index", len(time_mapping))
        
        if num_slices == 0:
            print("Array has no recorded slices, nothing to copy.")
        else:
            print(f"Copying {num_slices} time slices...")
            batch_size = 50 
            for i in range(0, num_slices, batch_size):
                end_idx = min(i + batch_size, num_slices)
                print(f"  Processing slices {i} to {end_idx-1}...")
                data = src_array[i:end_idx, :, :]
                with tiledb.DenseArray(temp_uri, mode='w') as dest_array:
                    dest_array[i:end_idx, :, :] = data

    # Verification Step
    print("Verifying data integrity...")
    with tiledb.DenseArray(array_uri, mode='r') as src:
        with tiledb.DenseArray(temp_uri, mode='r') as dest:
            # Check a few random slices
            for test_idx in [0, num_slices // 2, num_slices - 1]:
                if test_idx < 0 or test_idx >= num_slices: continue
                print(f"  Checking slice {test_idx}...")
                s_data = src[test_idx]
                d_data = dest[test_idx]
                
                # Handle cases where TileDB returns a dictionary of arrays
                if isinstance(s_data, dict): s_data = next(iter(s_data.values()))
                if isinstance(d_data, dict): d_data = next(iter(d_data.values()))
                
                if not np.allclose(s_data, d_data, equal_nan=True):
                    raise ValueError(f"Data mismatch at slice {test_idx}!")
    
    print("Verification passed.")

    # Swap arrays
    print(f"Backing up original to {backup_uri}...")
    os.rename(array_uri, backup_uri)
    print(f"Moving optimized array from {temp_uri} to {array_uri}...")
    # shutil.move is safer if temp_uri is on a different drive
    shutil.move(temp_uri, array_uri)
    
    # Calculate savings
    old_size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                   for dirpath, _, filenames in os.walk(backup_uri) 
                   for filename in filenames)
    new_size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                   for dirpath, _, filenames in os.walk(array_uri) 
                   for filename in filenames)
    
    print(f"Optimization complete!")
    print(f"Old size: {old_size / (1024**2):.2f} MB")
    print(f"New size: {new_size / (1024**2):.2f} MB")
    print(f"Reduction: {(1 - new_size/old_size)*100:.1f}%")
    print(f"You can now safely delete the backup: {backup_uri}")

if __name__ == "__main__":
    base_dir = r"c:\SCIPE\HCDP-data-for-AI\database"
    arrays = ["rainfall_array", "temperature_array", "spi_array"]
    
    for array_name in arrays:
        uri = os.path.join(base_dir, array_name)
        if os.path.exists(uri):
            try:
                optimize_array(uri)
            except Exception as e:
                print(f"Failed to optimize {array_name}: {e}")
