# src/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file located in the parent directory
# Assumes .env is in the project root (one level up from src)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env') 
load_dotenv(dotenv_path=dotenv_path)

# Load the Gemini API Key from environment variable (now loaded from .env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# You can add other configurations here, like model name, temperature, etc.
GEMINI_MODEL_NAME = "gemini-2.0-flash" # Or another suitable model
