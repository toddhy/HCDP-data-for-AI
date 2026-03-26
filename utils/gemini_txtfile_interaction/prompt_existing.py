from google import genai

client = genai.Client()
# Fetch all files
print("Fetching uploaded files...")
files = []
for file in client.files.list():
    if file.state.name == 'ACTIVE':
        files.append(file)
    else:
        print(f"Skipping {file.display_name} (State: {file.state})")

if not files:
    print("No active files found. Please upload files first.")
    exit()

print(f"Using {len(files)} files as context.")

# Define your question
question = input("\nEnter prompt for Gemini: ")

if not question.strip():
    print("No question provided. Exiting.")
    exit()

# Generate response using all files as context
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[question] + files
)

print("\n--- GEMINI RESPONSE ---\n")
print(response.text)
