"""
Rutas de chat (mensajes con IA)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import User, Conversation, Message
from ..schemas import ChatRequest, ChatResponse, MessageResponse
from ..auth import get_current_user
from ..ai_service import ai_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Envía un mensaje al chatbot y recibe una respuesta
    
    Si se proporciona conversation_id, añade el mensaje a esa conversación.
    Si no, crea una nueva conversación.
    """
    
    # 1. Obtener o crear conversación
    if chat_request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == chat_request.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversación no encontrada"
            )
    else:
        # Crear nueva conversación
        title = ai_service.generate_conversation_title(chat_request.message)
        conversation = Conversation(
            title=title,
            user_id=current_user.id
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    
    # 2. Guardar mensaje del usuario
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=chat_request.message
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # 3. Obtener historial de mensajes para contexto
    messages_history = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at.asc()).all()
    
    # Convertir a formato para la IA
    messages_for_ai = [
        {"role": msg.role, "content": msg.content}
        for msg in messages_history
    ]
    
    # 4. Generar respuesta de la IA
    try:
        ai_response = await ai_service.generate_response(messages_for_ai)
    except Exception as e:
        # Si falla la IA, eliminar el mensaje del usuario y lanzar error
        db.delete(user_message)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error al generar respuesta: {str(e)}"
        )
    
    # 5. Guardar respuesta del asistente
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response
    )
    db.add(assistant_message)
    
    # 6. Actualizar timestamp de la conversación
    conversation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(assistant_message)
    
    # 7. Retornar respuesta
    return ChatResponse(
        conversation_id=conversation.id,
        user_message=MessageResponse.from_orm(user_message),
        assistant_message=MessageResponse.from_orm(assistant_message)
    )


@router.get("/history/{conversation_id}")
async def get_chat_history(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial completo de mensajes de una conversación
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
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()
    
    return {
        "conversation_id": conversation_id,
        "title": conversation.title,
        "messages": [MessageResponse.from_orm(msg) for msg in messages]
    }
