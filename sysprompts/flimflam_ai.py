import os
import base64
import asyncio
import aiofiles
import hashlib

from google.genai import types
from dotenv import load_dotenv

from client import get_client
from config import get_generate_content_config

# Load environment variables from .env file
load_dotenv()

# Cache the system prompt and its content hash to avoid re-reading
_system_prompt_cache = None
_prompt_hash_cache = None

def _get_hash_cache_file():
    """Get the path to the hash cache file"""
    return os.path.join(os.path.dirname(__file__), ".system_prompt_hash")

def _load_persisted_hash():
    """Load the persisted hash from disk"""
    hash_file = _get_hash_cache_file()
    try:
        with open(hash_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except Exception:
        return None

def _save_persisted_hash(hash_value):
    """Save the hash to disk"""
    hash_file = _get_hash_cache_file()
    try:
        with open(hash_file, 'w', encoding='utf-8') as f:
            f.write(hash_value)
    except Exception:
        pass  # Silently fail if we can't write cache

async def load_system_prompt(timeout_seconds=30):
    """Load the system prompt from external file with caching and dynamic reloading based on content hash."""
    global _system_prompt_cache, _prompt_hash_cache
    
    prompt_file = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
    
    try:
        async with asyncio.timeout(timeout_seconds):
            async with aiofiles.open(prompt_file, 'r', encoding='utf-8') as f:
                current_content = await f.read()
        
        # Calculate hash of current content
        current_hash = hashlib.sha256(current_content.encode('utf-8')).hexdigest()
        
        # Load persisted hash on first run
        if _prompt_hash_cache is None:
            _prompt_hash_cache = _load_persisted_hash()
        
        if _prompt_hash_cache is None:
            print("📝 Loading system prompt for the first time...")
            _system_prompt_cache = current_content
            _prompt_hash_cache = current_hash
            _save_persisted_hash(current_hash)
        elif _prompt_hash_cache != current_hash:
            print("\n🔄 System prompt content changed. Reloading...")
            _system_prompt_cache = current_content
            _prompt_hash_cache = current_hash
            _save_persisted_hash(current_hash)
        # If hashes match, use cached content (no action needed)
            
        return _system_prompt_cache
        
    except asyncio.TimeoutError:
        # If we have cached content, return it instead of failing
        if _system_prompt_cache is not None:
            print(f"⚠️  Timeout loading system prompt, using cached version")
            return _system_prompt_cache
        raise Exception(f"Timeout loading system prompt after {timeout_seconds}s")
    except FileNotFoundError:
        raise Exception(f"System prompt file not found: {prompt_file}")
    except UnicodeDecodeError as e:
        raise Exception(f"Error decoding system prompt file (encoding issue): {str(e)}")
    except Exception as e:
        # If we have cached content, return it for resilience
        if _system_prompt_cache is not None:
            print(f"⚠️  Error reloading system prompt, using cached version: {str(e)}")
            return _system_prompt_cache
        raise Exception(f"Error loading system prompt: {str(e)}")

async def generate_response(user_question, timeout_seconds=60):
    """Generate a response for a user question with comprehensive error handling"""
    try:
        client = get_client()

        # Load system prompt from external file
        system_prompt = await load_system_prompt()
        
        # Add a CoT trigger to the user question
        cot_trigger = "\n\nNow, think step-by-step before providing your final answer."
        
        model = os.getenv("MODEL", "gemini-2.5-flash-lite")  # Default fallback
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=system_prompt),
                    types.Part.from_text(text=f"\nUser Question: {user_question}{cot_trigger}")
                ]
            ),
        ]

        generate_content_config = get_generate_content_config()

        response = ""
        try:
            # Add timeout wrapper for the entire streaming operation
            async with asyncio.timeout(timeout_seconds):
                for chunk in client.models.generate_content_stream(
                    model=model,
                    contents=contents,
                    config=generate_content_config,
                ):
                    print(chunk.text, end="", flush=True)
                    response += chunk.text
        
        except asyncio.TimeoutError:
            print(f"\n\n⏰ Response generation timed out after {timeout_seconds}s")
            if response:
                print("Returning partial response...")
                return response
            else:
                raise Exception(f"No response received within {timeout_seconds} seconds")
        
        except Exception as stream_error:
            print(f"\n\n❌ Streaming error: {stream_error}")
            raise Exception(f"Failed to generate response: {stream_error}")
        
        return response
    
    except Exception as e:
        # Handle system prompt loading errors or other setup issues
        if "system prompt" in str(e).lower():
            raise Exception(f"System setup error: {e}")
        else:
            raise Exception(f"Response generation failed: {e}")

async def main():
    """Main interactive Q&A loop with async support"""
    print("🚀 Welcome to Flimflam AI!")
    print("Ask me anything about Flimflam testing library.")
    print("Type 'quit', 'exit', or 'q' to stop.\n")
    
    # Pre-load system prompt for better performance
    try:
        await load_system_prompt()
        print("✅ System prompt loaded and cached successfully")
    except Exception as e:
        print(f"❌ Error: Could not load system prompt: {e}")
        return
    
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
