import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SQL_DB_PATH = "parking_dynamic.db"
    VECTOR_DB_PATH = "parking_static.faiss"

settings = Settings()