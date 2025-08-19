# AI Research & Development

## Setup

### Prerequisites

1. **Authenticate with Google Cloud (Application Default Credentials):**
   ```bash
   gcloud auth application-default login
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and set your GOOGLE_CLOUD_PROJECT and MODEL
   ```

3. **Install dependencies:**
   
   **Option 1: Using pip (recommended for most users)**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```
   
   **Option 2: Using uv (faster alternative)**
   ```bash
   # Install uv (see https://docs.astral.sh/uv/)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Or on macOS with Homebrew: brew install uv
   uv sync
   ```

### Running the Applications

#### Browser Agent:
```bash
# With pip
python gemini_use_browser.py
# With uv
uv run python gemini_use_browser.py
```

#### Flimflam AI Assistant:
```bash
# With pip
python sysprompts/flimflam_ai.py
# With uv  
uv run python sysprompts/flimflam_ai.py
```

**Features:**
- Interactive Q&A about Flimflam testing library
- Comprehensive knowledge base with examples and best practices  
- Async streaming responses for better user experience
- System prompt loaded from external file for easy maintenance

#### Gemini CLI:
```bash
# Setup system prompt file
cp GEMINI.example.md GEMINI.md

# Export environment variables and run gemini
export $(cat .env | xargs) && gemini
```

## Environment Variables

- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Platform project ID
- `MODEL`: AI model to use (e.g., "gemini-2.5-flash-lite")