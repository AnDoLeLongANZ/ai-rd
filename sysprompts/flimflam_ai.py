import os
import base64
import asyncio
import aiofiles

from google.genai import types
from dotenv import load_dotenv

from client import get_client
from config import get_generate_content_config

# Load environment variables from .env file
load_dotenv()

# Cache the system prompt to avoid re-reading
_system_prompt_cache = None

async def load_system_prompt(timeout_seconds=30):
    """Load the system prompt from external file with caching and timeout"""
    global _system_prompt_cache
    
    if _system_prompt_cache is not None:
        return _system_prompt_cache
    
    prompt_file = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
    
    try:
        # Add timeout wrapper for file operations
        async with asyncio.timeout(timeout_seconds):
            async with aiofiles.open(prompt_file, 'r', encoding='utf-8') as f:
                _system_prompt_cache = await f.read()
        return _system_prompt_cache
    except asyncio.TimeoutError:
        raise Exception(f"Timeout loading system prompt after {timeout_seconds}s")
    except FileNotFoundError:
        raise Exception(f"System prompt file not found: {prompt_file}")
    except Exception as e:
        raise Exception(f"Error loading system prompt: {str(e)}")

async def generate_response(user_question):
    """Generate a response for a user question"""
    client = get_client()

    # Load system prompt from external file
    system_prompt = await load_system_prompt()
    
    model = os.getenv("MODEL", "gemini-2.5-flash-lite")  # Default fallback
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=system_prompt),
                types.Part.from_text(text=f"\nUser Question: {user_question}")
            ]
        ),
    ]

    generate_content_config = get_generate_content_config()

    response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="", flush=True)
        response += chunk.text
    
    return response

async def main():
    """Main interactive Q&A loop with async support"""
    print("🚀 Welcome to Flimflam AI!")
    print("Ask me anything about Flimflam testing library.")
    print("Type 'quit', 'exit', or 'q' to stop.\n")
    
    # Pre-load system prompt for better performance
    try:
        await load_system_prompt()
        print("✅ System prompt loaded successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not pre-load system prompt: {e}")
    
    while True:
        try:
            # Get user input (this is inherently blocking, but that's okay)
            user_input = input("\n🤔 Your question: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q', '']:
                print("\n👋 Thanks for using Flimflam AI! Happy testing!")
                break
            
            # Generate and display response asynchronously
            print(f"\n🤖 Flimflam AI: ", end="", flush=True)
            await generate_response(user_input)
            print("\n" + "="*60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Happy testing!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or check your configuration.")

def run():
    """Entry point that handles the asyncio event loop"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy testing!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    run()