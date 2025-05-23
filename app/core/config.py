import os
from dotenv import load_dotenv

load_dotenv()

def get_openrouter_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the environment.")
    return key 