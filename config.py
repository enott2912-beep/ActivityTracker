import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AI_MODE = os.getenv('AI_MODE', 'ollama')  # Options: 'deepseek', 'ollama', 'openai', or None

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db', 'activitytracker.db')