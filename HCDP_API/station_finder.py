import pandas as pd
import sqlite3
import math

# --- Configuration ---
# Example: Near Hilo, Hawaii
target_lat, target_lon = 19.6728, -156.0203
radius_km = 10.0

# Set Pandas options to display all rows and columns without truncation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points 
    on the Earth (specified in decimal degrees) in kilometers.
    """
    R = 6371  # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))



# Create a connection to the SQLite database
conn = sqlite3.connect(r'C:\SCIPE\my_maps\my_database.db')

# --- 1. Calculate Bounding Box (Pre-filter) ---
# 1 degree lat is ~111km. 
lat_delta = radius_km / 111.0
# 1 deg lon at this lat is ~111km * cos(lat)
lon_delta = radius_km / (111.0 * math.cos(math.radians(target_lat)))

lat_min, lat_max = target_lat - lat_delta, target_lat + lat_delta
lon_min, lon_max = target_lon - lon_delta, target_lon + lon_delta

# --- 2. Query Database with Bounding Box ---
query_spatial = """
SELECT skn, name, lat, lng 
FROM hcd_stations 
WHERE lat BETWEEN ? AND ? 
  AND lng BETWEEN ? AND ?
"""

df_spatial = pd.read_sql_query(query_spatial, conn, params=(lat_min, lat_max, lon_min, lon_max))

# --- 3. Refine with Exact Haversine Distance ---
if not df_spatial.empty:
    df_spatial['distance_km'] = df_spatial.apply(
        lambda row: haversine(target_lat, target_lon, row['lat'], row['lng']), 
        axis=1
    )
    
    # Filter to only those truly within the circle and sort by distance
    df_result = df_spatial[df_spatial['distance_km'] <= radius_km].sort_values('distance_km')
    
    print(f"Stations within {radius_km}km of ({target_lat}, {target_lon}):")
    print(df_result.to_string())


else:
    print(f"No stations found within {radius_km}km of ({target_lat}, {target_lon}).")

# Close the connection
conn.close()
