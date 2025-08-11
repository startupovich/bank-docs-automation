import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    # Настройки базы данных
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "bank_docs")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    
    # Настройки очереди
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "documents_queue")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
    
    # Пути к данным
    BASE_DIR = Path(__file__).resolve().parent.parent
    INPUT_DIR = BASE_DIR / os.getenv("INPUT_DIR", "data/input")
    PROCESSED_DIR = BASE_DIR / os.getenv("PROCESSED_DIR", "data/processed")
    FAILED_DIR = BASE_DIR / os.getenv("FAILED_DIR", "data/failed")
    
    # Настройки обработки
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 10))  # секунды
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    
    # Уровень логгирования
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def DB_URL(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

config = Config()