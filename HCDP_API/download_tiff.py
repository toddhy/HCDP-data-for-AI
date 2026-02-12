import requests
import rasterio
from io import BytesIO
import argparse

# You'll need an API key - sign up at:
# https://www.hawaii.edu/climate-data-portal/hcdp-hawaii-mesonet-api/

API_BASE_URL = "https://api.hcdp.ikewai.org"  # This may vary

def download_tiff(endpoint, params, output_file, api_key):
    """
    Download a TIFF file from the HCDP API
    
    Args:
        endpoint: API endpoint (e.g., "/rainfall/daily")
        params: Query parameters (date, region, etc.)
        output_file: Where to save the TIFF
        api_key: HCDP API Key
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(
        f"{API_BASE_URL}{endpoint}",
        params=params,
        headers=headers
    )
    
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {output_file}")
        return output_file
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download TIFF from HCDP API")
    parser.add_argument("api_key", help="HCDP API Key")
    args = parser.parse_args()

    # Example usage (adjust based on actual need)
    params = {
        "date": "2024-01-15",
        "variable": "station_ids",
        "format": "tiff"
    }

    download_tiff("/mesonet/db/measurements", params, "rainfall_20240115.tif", args.api_key)
