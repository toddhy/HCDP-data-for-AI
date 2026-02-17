import os
import serpapi
import sys
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    print("--- SerpAPI Publication Downloader ---")
    
    # Get API key from environment or prompt user
    api_key = os.getenv("SerpApi")
    if not api_key:
        print("SerpAPI Key not found in environment variables.")
        api_key = input("Please enter your SerpAPI Key: ").strip()
    
    if not api_key:
        print("Error: API Key is required to run this script.")
        return

    max_results = 70  # Set your chosen max value here
    start_offset = 0
    total_found_count = 0
    output_filename = "scholar_results.txt"

    print(f"Searching Google Scholar via SerpAPI (up to {max_results} results)...")
    print(f"Results will be saved to: {output_filename}")
    
    try:
        client = serpapi.Client(api_key=api_key)
        
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(f"--- SerpAPI Publication Results ---\n")
            f.write(f"Max Results: {max_results}\n\n")

            while start_offset < max_results:
                print(f"\n--- Fetching results starting at offset: {start_offset} ---")
                params = {
                    "engine": "google_scholar",
                    "num": "10",
                    "start": str(start_offset),
                    "oi": "bibs",
                    "cites": "11258593421370337345",
                    "hl": "en",
                }

                results = client.search(params).as_dict()

                if "organic_results" in results:
                    for result in results["organic_results"]:
                        title = result.get("title")
                        link = result.get("link")
                        resources = result.get("resources")

                        # Console output
                        print(f"\nTitle: {title}")
                        print(f"Main Link: {link}")
                        
                        # File output
                        f.write(f"Title: {title}\n")
                        f.write(f"Main Link: {link}\n")

                        if resources:
                            for resource in resources:
                                res_link = resource.get("link")
                                res_format = resource.get("file_format", "Web")
                                print(f"  [{res_format} Found]: {res_link}")
                                f.write(f"  [{res_format}]: {res_link}\n")
                                total_found_count += 1
                        
                        f.write("-" * 30 + "\n")
                        print("-" * 20)
                    
                    if not results.get("organic_results"):
                        print("No more results available.")
                        f.write("\nNo more results available from SerpAPI.\n")
                        break
                else:
                    print("No results found or an error occurred in the search.")
                    f.write("\nNo results found or search terminated.\n")
                    break
                
                start_offset += 10
            
            f.write(f"\nSearch complete. Total resource links found: {total_found_count}\n")
            
        print(f"\nSearch complete. Total resource links found: {total_found_count}")
        print(f"All details have been saved to {output_filename}")

    except Exception as e:
        if "401" in str(e):
            print("\nError: Invalid API Key (401 Unauthorized).")
        elif "403" in str(e):
            print("\nError: API Key is blocked or quota exceeded (403 Forbidden).")
        else:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

