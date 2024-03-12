from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os

# env_path = Path(".") / ".env"

load_dotenv(find_dotenv())

# env vars
class Config:
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")

