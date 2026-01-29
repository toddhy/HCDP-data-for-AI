import pathlib
from google import genai
from google.genai import types

client = genai.Client()
MODEL_ID = "gemini-2.0-flash"

files = []
# Searching for .txt files
path_to_search = r"path/to/files"
print(f"Uploading files from {path_to_search}...")

for p in pathlib.Path(path_to_search).rglob('*.txt'):
    if 'test' in str(p):
        continue
    f = client.files.upload(file=p, config={'display_name': p.name})
    # Use Content/Part structure or URI directly if supported
    files.append(f)
    print('.', end='', flush=True)

if not files:
    print("\nNo files found! Check the directory path and file extension.")
    exit()

print(f"\nUploaded {len(files)} files. Generating summary...")

# We can pass the file objects directly in the contents list
# The model will see them as parts of the request.
response = client.models.generate_content(
    model=MODEL_ID,
    contents=["Summarize these texts"] + files
)

print("\n--- GEMINI RESPONSE ---\n")
print(response.text)