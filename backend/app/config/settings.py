import os


class Config:
    """Конфигурация приложения Flask"""
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or f"sqlite:///{os.path.join(BASE_DIR, '..', 'instance', 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY") or "dev"
    
    LOG_LEVEL = os.getenv("LOG_LEVEL") or "INFO"