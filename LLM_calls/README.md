# LLM Calls

This directory contains scripts for interacting with the Gemini API using the `google-genai` File API.

## Scripts

### 1. `fileAPI_uploader.py`
Uploads local text files to the Gemini File API.
- **Functionality**: Scans a specified directory for `.txt` files and uploads them to your Gemini account.
- **Initial Prompt**: After uploading, it sends a command to Gemini to summarize the uploaded texts as separate documents.
- **Usage**: Update the `path_to_search` variable in the script to point to your local text files.

### 2. `prompt_existing.py`
Interaction with already uploaded files.
- **Functionality**: Fetches all previously uploaded files that are in an `ACTIVE` state.
- **Interactive**: Prompts the user to enter a question in the terminal.
- **Context**: Sends the user's question to Gemini (`gemini-2.0-flash`) along with all the active files as context for the answer.

## Requirements
- Python 3.10+
- `google-genai` library installed
- An active Google GenAI API Key configured in your environment.
