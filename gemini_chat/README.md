# Gemini interaction

This directory contains scripts for interacting with the Gemini API using the `google-genai` File API.

## Scripts

### 1. `fileAPI_uploader.py`
Uploads local text files to the Gemini File API.
- **Functionality**: Scans a directory for `.txt` files and uploads them.
- **CLI Argument**: accepts `--path` to specify the search directory (defaults to current directory).
- **Initial Prompt**: Generates an initial summary of uploaded texts.
- **Usage**: `python fileAPI_uploader.py --path /your/data/folder`

### 2. `chatbot.py`
Continuous chat session using all active uploaded files as context.
- **Functionality**: Fetches active files and starts an interactive chat.
- **Memory**: Maintains conversation history within the session.
- **Usage**: `python chatbot.py`

### 3. `prompt_existing.py`
Single-turn interaction with already uploaded files.
- **Functionality**: Fetches `ACTIVE` files and prompts for a single question.
- **Usage**: `python prompt_existing.py`

## Requirements
- Python 3.10+
- `google-genai` library installed
- An active Google GenAI API Key (`GOOGLE_API_KEY`) configured in your environment.
- Model: These scripts use `gemini-2.5-flash`.
