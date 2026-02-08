import os
from google import genai
from google.genai import types

def run_chatbot():
    client = genai.Client()
    MODEL_ID = "gemini-2.5-flash"

    # 1. Fetch uploaded files
    print("Fetching active uploaded files...")
    files = []
    try:
        for file in client.files.list():
            if file.state.name == 'ACTIVE':
                files.append(file)
            else:
                print(f"Skipping {file.display_name} (State: {file.state})")
    except Exception as e:
        print(f"Error fetching files: {e}")
        return

    if not files:
        print("No active files found. Please run fileAPI_uploader.py first.")
        return

    print(f"Using {len(files)} files as context.")
    for f in files:
        print(f" - {f.display_name}")

    # 2. Initialize chat session with files as context
    # Note: We provide the files in the history or as initial context parts.
    # In the current SDK, we can start a chat and pass the files in the first message or as context.
    chat = client.chats.create(model=MODEL_ID)

    print("\n--- CHATBOT READY ---")
    print("Type 'exit' or 'quit' to end the session.\n")

    history_with_files = False

    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        if not user_input.strip():
            continue

        try:
            # If it's the first message, include the files for context
            if not history_with_files:
                contents = files + [user_input]
                response = chat.send_message(message=contents)
                history_with_files = True
            else:
                response = chat.send_message(user_input)
            
            print(f"\nGemini: {response.text}\n")
        except Exception as e:
            print(f"Error during chat: {e}")

if __name__ == "__main__":
    run_chatbot()
