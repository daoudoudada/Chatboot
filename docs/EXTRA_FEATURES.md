# ⭐ Features Extras (Opcional pero Brutal)

Esta guía muestra cómo agregar características avanzadas a tu chatbot.

## 🌙 Dark Mode

### Backend
No requiere cambios.

### Frontend

1. **Añadir estilos dark en `styles.css`:**

```css
/* Añadir al final del archivo */

/* Dark Mode Variables */
[data-theme="dark"] {
    --primary-color: #10a37f;
    --primary-dark: #0d8c6d;
    --background: #1a1a1a;
    --surface: #2d2d2d;
    --surface-hover: #3d3d3d;
    --text-primary: #e5e5e5;
    --text-secondary: #a0a0a0;
    --border: #404040;
    --shadow: rgba(0, 0, 0, 0.3);
    --shadow-lg: rgba(0, 0, 0, 0.5);
}

/* Dark Mode Toggle Button */
.theme-toggle {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: var(--primary-color);
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 4px 12px var(--shadow-lg);
    transition: var(--transition);
    z-index: 1000;
}

.theme-toggle:hover {
    transform: scale(1.1);
}
```

2. **Añadir botón en `index.html`:**

```html
<!-- Antes del cierre de </body> -->
<button class="theme-toggle" id="theme-toggle">🌙</button>
```

3. **Añadir JavaScript en `app.js`:**

```javascript
// Al final del archivo, antes del window.addEventListener

// Dark Mode Toggle
const themeToggle = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme') || 'light';

// Aplicar tema guardado
document.documentElement.setAttribute('data-theme', currentTheme);
themeToggle.textContent = currentTheme === 'dark' ? '☀️' : '🌙';

themeToggle.addEventListener('click', () => {
    const theme = document.documentElement.getAttribute('data-theme');
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    themeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
});
```

## 📥 Exportar Conversaciones

### Backend

Añade una nueva ruta en `backend/routes/conversations.py`:

```python
from fastapi.responses import FileResponse
import json
from datetime import datetime

@router.get("/{conversation_id}/export")
async def export_conversation(
    conversation_id: int,
    format: str = "txt",  # txt, json, md
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exporta una conversación en diferentes formatos
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()
    
    filename = f"conversation_{conversation_id}_{datetime.now().strftime('%Y%m%d')}"
    
    if format == "json":
        content = {
            "title": conversation.title,
            "created_at": str(conversation.created_at),
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": str(msg.created_at)
                }
                for msg in messages
            ]
        }
        
        with open(f"/tmp/{filename}.json", "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        return FileResponse(
            f"/tmp/{filename}.json",
            filename=f"{filename}.json",
            media_type="application/json"
        )
    
    elif format == "md":
        lines = [f"# {conversation.title}\n"]
        lines.append(f"*Creado: {conversation.created_at}*\n\n")
        
        for msg in messages:
            role = "👤 Usuario" if msg.role == "user" else "🤖 Asistente"
            lines.append(f"### {role}\n")
            lines.append(f"{msg.content}\n\n")
            lines.append(f"*{msg.created_at}*\n\n---\n\n")
        
        content = "\n".join(lines)
        
        with open(f"/tmp/{filename}.md", "w", encoding="utf-8") as f:
            f.write(content)
        
        return FileResponse(
            f"/tmp/{filename}.md",
            filename=f"{filename}.md",
            media_type="text/markdown"
        )
    
    else:  # txt
        lines = [f"{conversation.title}\n"]
        lines.append(f"Creado: {conversation.created_at}\n")
        lines.append("=" * 50 + "\n\n")
        
        for msg in messages:
            role = "USUARIO" if msg.role == "user" else "ASISTENTE"
            lines.append(f"[{role}] - {msg.created_at}\n")
            lines.append(f"{msg.content}\n\n")
            lines.append("-" * 50 + "\n\n")
        
        content = "\n".join(lines)
        
        with open(f"/tmp/{filename}.txt", "w", encoding="utf-8") as f:
            f.write(content)
        
        return FileResponse(
            f"/tmp/{filename}.txt",
            filename=f"{filename}.txt",
            media_type="text/plain"
        )
```

### Frontend

Añade botones de exportación en `index.html` (dentro de conversation-item):

```html
<div class="conversation-actions">
    <button class="conversation-export" data-id="${conv.id}" data-format="txt">
        📄
    </button>
    <button class="conversation-export" data-id="${conv.id}" data-format="md">
        📝
    </button>
    <button class="conversation-export" data-id="${conv.id}" data-format="json">
        📊
    </button>
</div>
```

Añade la función en `app.js`:

```javascript
// Exportar conversación
document.querySelectorAll('.conversation-export').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        e.stopPropagation();
        const convId = btn.dataset.id;
        const format = btn.dataset.format;
        
        try {
            const response = await fetch(
                `${API_URL}/conversations/${convId}/export?format=${format}`,
                {
                    headers: {
                        'Authorization': `Bearer ${authToken}`
                    }
                }
            );
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `conversation_${convId}.${format}`;
            a.click();
            
            showToast(`Conversación exportada como ${format.toUpperCase()}`, 'success');
        } catch (error) {
            showToast('Error al exportar', 'error');
        }
    });
});
```

## 🔍 Búsqueda en Conversaciones

### Backend

Añade en `backend/routes/conversations.py`:

```python
@router.get("/search/{query}")
async def search_conversations(
    query: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Busca en títulos y mensajes de conversaciones
    """
    # Buscar en títulos
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.title.ilike(f"%{query}%")
    ).all()
    
    # Buscar en mensajes
    messages = db.query(Message).join(Conversation).filter(
        Conversation.user_id == current_user.id,
        Message.content.ilike(f"%{query}%")
    ).all()
    
    # Obtener conversaciones únicas de los mensajes
    conv_ids_from_messages = {msg.conversation_id for msg in messages}
    convs_from_messages = db.query(Conversation).filter(
        Conversation.id.in_(conv_ids_from_messages)
    ).all()
    
    # Combinar resultados
    all_conversations = list({conv.id: conv for conv in conversations + convs_from_messages}.values())
    
    return [ConversationResponse.from_orm(conv) for conv in all_conversations]
```

### Frontend

Añade barra de búsqueda en `index.html`:

```html
<!-- Después de sidebar-header -->
<div class="search-bar">
    <input type="text" id="search-input" placeholder="🔍 Buscar conversaciones...">
</div>
```

CSS en `styles.css`:

```css
.search-bar {
    padding: 12px 20px;
    border-bottom: 1px solid var(--border);
}

.search-bar input {
    width: 100%;
    padding: 10px 14px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-size: 0.9rem;
}
```

JavaScript en `app.js`:

```javascript
let searchTimeout;
const searchInput = document.getElementById('search-input');

searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    const query = e.target.value.trim();
    
    if (query.length < 2) {
        loadConversations();
        return;
    }
    
    searchTimeout = setTimeout(async () => {
        try {
            const results = await apiRequest(`/conversations/search/${query}`);
            renderConversations(results);
        } catch (error) {
            showToast('Error en la búsqueda', 'error');
        }
    }, 300);
});
```

## 👤 Perfil de Usuario

### Backend

Añade rutas en `backend/routes/auth.py`:

```python
from ..schemas import UserUpdate

# Schema nuevo en schemas.py:
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

@router.put("/me", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza el perfil del usuario"""
    if user_data.username:
        current_user.username = user_data.username
    if user_data.email:
        current_user.email = user_data.email
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Estadísticas del usuario"""
    total_conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).count()
    
    total_messages = db.query(Message).join(Conversation).filter(
        Conversation.user_id == current_user.id
    ).count()
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "member_since": current_user.created_at
    }
```

### Frontend

Añade modal de perfil en `index.html`:

```html
<!-- Modal de perfil -->
<div id="profile-modal" class="modal">
    <div class="modal-content">
        <span class="close">&times;</span>
        <h2>Mi Perfil</h2>
        <div id="profile-info"></div>
    </div>
</div>
```

## 📊 Estadísticas de Uso

Muestra gráficos con:
- Total de conversaciones
- Total de mensajes
- Mensajes por día
- Temas más consultados

Usa libraries como [Chart.js](https://www.chartjs.org/) en el frontend.

## 🎤 Entrada por Voz

Usa Web Speech API:

```javascript
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'es-ES';

document.getElementById('voice-btn').addEventListener('click', () => {
    recognition.start();
});

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    messageInput.value = transcript;
};
```

## 🔔 Notificaciones Push

Implementa con Service Workers para notificar cuando hay una respuesta.

## 📱 PWA (Progressive Web App)

Convierte tu app en instalable añadiendo:
- `manifest.json`
- Service Worker
- Iconos

---

¿Quieres implementar alguna de estas? ¡Consulta la documentación específica de cada feature!
