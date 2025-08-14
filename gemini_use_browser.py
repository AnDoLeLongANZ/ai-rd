import asyncio
import subprocess
import sys
import os
from dotenv import load_dotenv

from browser_use import Agent
from browser_use.llm import ChatGoogle

# Load environment variables from .env file
load_dotenv()

def install_playwright_browsers():
    """Install Playwright browsers if not already installed."""
    try:
        print("Installing Playwright browsers...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        print("✅ Playwright browsers installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Playwright browsers: {e}")
        raise


async def example_gemini_vertex():
    """Example using ChatGoogle - convenience class for Gemini models."""
 
    llm = ChatGoogle(
        model='gemini-2.5-flash',
        location='us-central1',
        temperature=0.1,
        project=os.getenv("GCLOUD_PROJECT"),
        vertexai=True
    )
    return llm
 
tasks = """
1. go to google.com
2. search for 'ANZ Plus'
"""

async def run_agent(llm):
    agent = Agent(
        task=tasks,
        llm=llm,
    )

    print("Task: Navigate to google.com and search for 'ANZ Plus'")

    result = await agent.run(max_steps=4)
    print(f'Result: {result}')
 
 
async def main():
    """Run Google Gemini examples."""
    try:
        # Install Playwright browsers first
        install_playwright_browsers()
        
        llm = await example_gemini_vertex()
        await run_agent(llm)
    except FileNotFoundError as e:
        if "Chromium" in str(e):
            print("❌ Chromium browser not found. Please run: playwright install chromium")
            print("Or try: python -m playwright install chromium")
        else:
            print(f'❌ File not found error: {e}')
    except Exception as e:
        print(f'❌ Error: {e}')
 
 
if __name__ == '__main__':
    asyncio.run(main())