import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================
# API Keys
# ==========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==========================
# LLM Configuration
# ==========================

MODEL_NAME = "llama-3.3-70b-versatile"

# ==========================
# Embedding Model
# ==========================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ==========================
# Directories
# ==========================

UPLOAD_FOLDER = "uploads"
CHROMA_DB_DIR = "chroma_db"