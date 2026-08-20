import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
APP_TITLE = "PaperLens"
APP_ICON = "◈"
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = ["pdf"]
