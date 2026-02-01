"""
Rutas de conversaciones
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Conversation, Message
from ..schemas import (
    ConversationCreate,
    ConversationResponse,
    ConversationWithMessages
)
from ..auth import get_current_user

router = APIRouter(prefix="/conversations", tags=["Conversaciones"])


@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea una nueva conversación
    """
    new_conversation = Conversation(
        title=conversation_data.title,
        user_id=current_user.id
    )
    
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    
    # Añadir contador de mensajes
    response = ConversationResponse.from_orm(new_conversation)
    response.message_count = 0
    
    return response


@router.get("/", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las conversaciones del usuario actual
    """
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.updated_at.desc()).all()
    
    # Añadir contador de mensajes a cada conversación
    result = []
    for conv in conversations:
        conv_response = ConversationResponse.from_orm(conv)
        conv_response.message_count = len(conv.messages)
        result.append(conv_response)
    
    return result


@router.get("/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene una conversación específica con todos sus mensajes
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada"
        )
    
    return conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina una conversación
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada"
        )
    
    db.delete(conversation)
    db.commit()
    
    return None


@router.put("/{conversation_id}/title", response_model=ConversationResponse)
async def update_conversation_title(
    conversation_id: int,
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza el título de una conversación
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada"
        )
    
    conversation.title = conversation_data.title
    db.commit()
    db.refresh(conversation)
    
    response = ConversationResponse.from_orm(conversation)
    response.message_count = len(conversation.messages)
    
    return response
