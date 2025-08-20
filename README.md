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
   ```

3. **If you are running this project behing a proxy**
   ```bash
   # Verify your /etc/hosts file for any proxy-related configurations
   # that might affect network connections to Google Cloud services
   cat /etc/hosts
   ```

4. **Install dependencies:**
   ```bash
   # Install uv (see https://docs.astral.sh/uv/)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Or on macOS with Homebrew: brew install uv
   uv sync
   ```

### Running the Applications

#### Browser Agent:
```bash
python gemini_use_browser.py
```

#### Flimflam AI Assistant:
   ```bash
   # Setup system prompt file
   cp sysprompts/system_prompt.keep sysprompts/system_prompt.txt
   # Edit sysprompts/system_prompt.txt with your desired system prompt

   python sysprompts/flimflam_ai.py
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
