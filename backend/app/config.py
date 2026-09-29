import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

class Settings:
    PROJECT_NAME: str = "Field Service Memory"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "The Technician Who Never Forgets — Persistent Organizational Memory for Field Service"

    # Database
    DATABASE_PATH: Path = DATA_DIR / "field_service_memory.db"
    DATABASE_URL: str = f"sqlite:///{DATA_DIR}/field_service_memory.db"

    # Hindsight Configuration (vectorize.io)
    HINDSIGHT_API_URL: str = os.environ.get("HINDSIGHT_API_URL", "https://api.hindsight.vectorize.io")
    HINDSIGHT_API_KEY: str = os.environ.get("HINDSIGHT_API_KEY", "")
    HINDSIGHT_BANK_ID: str = os.environ.get("HINDSIGHT_BANK_ID", "field-service-org-memory")

    # Gemini / LLM Configuration
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

settings = Settings()
