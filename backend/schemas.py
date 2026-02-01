"""
Schemas de Pydantic para validación de datos
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

# ===== USER SCHEMAS =====

class UserCreate(BaseModel):
    """Schema para crear usuario"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema de respuesta de usuario"""
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema de token JWT"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Datos del token"""
    user_id: Optional[int] = None


# ===== CONVERSATION SCHEMAS =====

class ConversationCreate(BaseModel):
    """Schema para crear conversación"""
    title: Optional[str] = "Nueva conversación"

class ConversationResponse(BaseModel):
    """Schema de respuesta de conversación"""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


# ===== MESSAGE SCHEMAS =====

class MessageCreate(BaseModel):
    """Schema para crear mensaje"""
    content: str = Field(..., min_length=1)

class MessageResponse(BaseModel):
    """Schema de respuesta de mensaje"""
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    """Schema para request de chat"""
    message: str = Field(..., min_length=1)
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    """Schema de respuesta de chat"""
    conversation_id: int
    user_message: MessageResponse
    assistant_message: MessageResponse


# ===== CONVERSATION WITH MESSAGES =====

class ConversationWithMessages(BaseModel):
    """Conversación completa con sus mensajes"""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True
