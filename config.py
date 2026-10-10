import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DSN = os.getenv("DB_DSN")
WALLET_DIR = os.getenv("WALLET_DIR")
WALLET_PASSWORD = os.getenv("WALLET_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Safety check: Ensure variables are loaded
if not DB_USER or not DB_PASSWORD:
    raise ValueError("❌ Database credentials missing in .env file")