"""
Servicio de integración con APIs de IA
Soporta OpenAI (ChatGPT) y Google Gemini
"""
from typing import List, Dict
from .config import settings
import requests
import json


class AIService:
    """Servicio para interactuar con APIs de IA"""
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.system_prompt = settings.SYSTEM_PROMPT
    
    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Genera respuesta usando el proveedor de IA configurado
        
        Args:
            messages: Lista de mensajes en formato [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            str: Respuesta generada por la IA
        """
        if self.provider == "openai":
            return await self._openai_generate(messages)
        elif self.provider == "gemini":
            return await self._gemini_generate(messages)
        else:
            raise ValueError(f"Proveedor de IA no soportado: {self.provider}")
    
    async def _openai_generate(self, messages: List[Dict[str, str]]) -> str:
        """Genera respuesta usando OpenAI API"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no configurada")
        
        # Preparar mensajes con system prompt
        full_messages = [{"role": "system", "content": self.system_prompt}] + messages
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": settings.AI_MODEL,
                    "messages": full_messages,
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
        except requests.RequestException as e:
            raise Exception(f"Error al comunicarse con OpenAI: {str(e)}")
    
    async def _gemini_generate(self, messages: List[Dict[str, str]]) -> str:
        """Genera respuesta usando Google Gemini API"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY no configurada")
        
        # Convertir mensajes al formato de Gemini
        gemini_messages = self._convert_to_gemini_format(messages)
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.AI_MODEL}:generateContent"
            
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                params={"key": settings.GEMINI_API_KEY},
                json={
                    "contents": gemini_messages,
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 1000
                    },
                    "systemInstruction": {
                        "parts": [{"text": self.system_prompt}]
                    }
                },
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
            
        except requests.RequestException as e:
            raise Exception(f"Error al comunicarse con Gemini: {str(e)}")
    
    def _convert_to_gemini_format(self, messages: List[Dict[str, str]]) -> List[Dict]:
        """Convierte mensajes de formato OpenAI a formato Gemini"""
        gemini_messages = []
        
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_messages.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        return gemini_messages
    
    def generate_conversation_title(self, first_message: str) -> str:
        """
        Genera un título automático para la conversación basado en el primer mensaje
        
        Args:
            first_message: Primer mensaje del usuario
        
        Returns:
            str: Título generado (máximo 50 caracteres)
        """
        # Tomar las primeras palabras del mensaje
        words = first_message.split()[:8]
        title = " ".join(words)
        
        # Truncar si es muy largo
        if len(title) > 50:
            title = title[:47] + "..."
        
        return title if title else "Nueva conversación"


# Instancia global del servicio
ai_service = AIService()
