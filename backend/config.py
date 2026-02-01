"""
Configuración de la aplicación
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Base de datos
    DATABASE_URL: str = "sqlite:///./ai_chatbot.db"
    # Para PostgreSQL usar: "postgresql://user:password@localhost/dbname"
    
    # JWT
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API de IA (elegir una)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # Configuración del chatbot
    AI_MODEL: str = "gpt-3.5-turbo"  # o "gemini-pro"
    AI_PROVIDER: str = "openai"  # o "gemini"
    
    # Sistema prompt personalizado
    SYSTEM_PROMPT: str = """Eres un asistente experto en análisis de datos y machine learning.
Tu objetivo es ayudar a los usuarios a:
- Entender conceptos de ML y data science
- Resolver problemas de análisis de datos
- Explicar algoritmos y técnicas
- Proporcionar código de ejemplo en Python

Siempre sé claro, didáctico y proporciona ejemplos prácticos.
"""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
