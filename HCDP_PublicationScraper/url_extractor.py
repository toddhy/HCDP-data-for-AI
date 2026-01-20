import requests
import re
import sys
import os

def extract_urls(content, start_marker, end_marker):
    """
    Extracts substrings that are found between the start_marker 
    and end_marker in the content.
    """
    # Escape markers to ensure they are treated as literal strings in regex
    start_escaped = re.escape(start_marker)
    end_escaped = re.escape(end_marker)
    
    # Pattern to find everything between the markers
    # (.*?) is a non-greedy match for any character
    pattern = f"{start_escaped}(.*?){end_escaped}"
    
    # re.DOTALL ensures '.' matches newlines as well, in case content spans lines
    matches = re.findall(pattern, content, re.DOTALL)
    
    return [match.strip() for match in matches]

def get_content(source):
    """
    Retrieves content from a URL or a local file path.
    """
    if source.startswith('http://') or source.startswith('https://'):
        print(f"Fetching content from URL: {source}...")
        try:
            response = requests.get(source)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None
    elif os.path.exists(source):
        print(f"Reading content from file: {source}...")
        try:
            with open(source, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    else:
        print("Error: Source is not a valid URL or file path.")
        return None

def main():
    print("--- Beginner Substring Extractor ---")
    
    # Ask the user for input
    print("Enter the URL (e.g., https://example.com) or local file path:")
    source = input("> ").strip()
    
    print("Enter the Start Substring:")
    start_marker = input("> ") # Don't strip, spaces might be significant
    
    print("Enter the End Substring:")
    end_marker = input("> ")   # Don't strip
    
    if not source or not start_marker or not end_marker:
        print("Error: Source, Start Substring, and End Substring are required.")
        return

    # Get the content
    content = get_content(source)
    
    if content:
        # Extract substrings
        results = extract_urls(content, start_marker, end_marker)
        
        # Display results
        if results:
            print(f"\nFound {len(results)} matches:")
            with open("output.txt", "w", encoding="utf-8") as f:
                for res in results:
                    print(f"- {res}")
                    f.write(f"{res}\n")
            print(f"\nResults have been written to 'output.txt'.")
        else:
            print(f"\nNo matches found between '{start_marker}' and '{end_marker}'.")

if __name__ == "__main__":
    main()
