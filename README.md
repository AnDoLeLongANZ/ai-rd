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
   # Edit .env and set your GCLOUD_PROJECT
   ```

3. **Install and sync dependencies (uv replaces pip):**
   ```bash
   # Install uv (see https://docs.astral.sh/uv/)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Or on macOS with Homebrew: brew install uv
   uv sync
   ```

### Running the Browser Agent

```bash
uv run python gemini_use_browser.py
```

### Dependency Management (uv)

- Add a package: `uv add <package>`
- Remove a package: `uv remove <package>`
- Sync after pyproject.toml changes: `uv sync`
- Export a requirements.txt (for interoperability):
  ```bash
  uv export --format=requirements-txt --no-hashes > requirements.txt
  ```

### Troubleshooting

If you encounter a Chromium browser error, install Playwright browsers:
```bash
uv run python -m playwright install chromium
```

## Environment Variables

- `GCLOUD_PROJECT`: Your Google Cloud Platform project ID