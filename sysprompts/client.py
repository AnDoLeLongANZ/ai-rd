import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_client():
    """Create and return a configured Google GenAI client"""
    return genai.Client(
        vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    )
