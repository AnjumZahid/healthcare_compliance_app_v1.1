import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# =====================
# 🔑 API Keys
# =====================
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# =====================
# ⚙️ Models
# =====================
DEFAULT_CHAT_MODEL = "gemini-2.5-flash"
FAST_CHAT_MODEL = "gemini-2.0-flash"
EMBEDDING_MODEL = "gemini-embedding-001"

# =====================
# 📂 Paths
# =====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
DB_DIR = os.path.join(BASE_DIR, "database")
IMG_MODEL_DIR = os.path.join(DATA_DIR, "models")


# =====================
# ⚖️ General App Settings
# =====================
MAX_RETRIEVED_CHUNKS = 2
FDA_SERVER_PORT = 8002
DEBUG_MODE = True
