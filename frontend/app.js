// ===== CONFIGURACIÓN =====
const API_URL = 'http://localhost:8000/api';
let authToken = localStorage.getItem('authToken');
let currentUser = null;
let currentConversationId = null;

// ===== ELEMENTOS DEL DOM =====
const authPage = document.getElementById('auth-page');
const chatPage = document.getElementById('chat-page');
const loginForm = document.getElementById('login');
const registerForm = document.getElementById('register');
const showRegisterBtn = document.getElementById('show-register');
const showLoginBtn = document.getElementById('show-login');
const loginFormDiv = document.getElementById('login-form');
const registerFormDiv = document.getElementById('register-form');
const logoutBtn = document.getElementById('logout-btn');
const newChatBtn = document.getElementById('new-chat-btn');
const conversationsList = document.getElementById('conversations-list');
const chatMessages = document.getElementById('chat-messages');
const welcomeScreen = document.getElementById('welcome-screen');
const chatInputContainer = document.getElementById('chat-input-container');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const loadingOverlay = document.getElementById('loading-overlay');
const userNameDisplay = document.getElementById('user-name');

// ===== UTILIDADES =====

function showLoading() {
    loadingOverlay.classList.add('active');
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    const container = document.getElementById('toast-container');
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (authToken) {
        defaultOptions.headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers,
            },
        });
        
        if (!response.ok) {
            try {
                const error = await response.json();
                throw new Error(error.detail || `Error ${response.status}: ${response.statusText}`);
            } catch (e) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error en apiRequest:', error);
        if (error.message.includes('Failed to fetch')) {
            throw new Error('No se puede conectar con el servidor. Verifica que el backend esté corriendo en http://localhost:8000');
        }
        throw error;
    }
}

function formatTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Ahora';
    if (diffMins < 60) return `Hace ${diffMins} min`;
    if (diffHours < 24) return `Hace ${diffHours}h`;
    if (diffDays < 7) return `Hace ${diffDays}d`;
    
    return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
}

// ===== AUTENTICACIÓN =====

showRegisterBtn.addEventListener('click', (e) => {
    e.preventDefault();
    loginFormDiv.classList.remove('active');
    registerFormDiv.classList.add('active');
});

showLoginBtn.addEventListener('click', (e) => {
    e.preventDefault();
    registerFormDiv.classList.remove('active');
    loginFormDiv.classList.add('active');
});

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    try {
        showLoading();
        await apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password }),
        });
        
        showToast('¡Cuenta creada exitosamente! Ahora inicia sesión', 'success');
        registerFormDiv.classList.remove('active');
        loginFormDiv.classList.add('active');
        registerForm.reset();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
});

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        showLoading();
        const data = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
        
        authToken = data.access_token;
        localStorage.setItem('authToken', authToken);
        
        await loadUserInfo();
        showChatPage();
        showToast('¡Bienvenido!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
});

logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('authToken');
    authToken = null;
    currentUser = null;
    currentConversationId = null;
    
    authPage.classList.add('active');
    chatPage.classList.remove('active');
    loginForm.reset();
    showToast('Sesión cerrada', 'info');
});

async function loadUserInfo() {
    try {
        currentUser = await apiRequest('/auth/me');
        userNameDisplay.textContent = currentUser.username;
    } catch (error) {
        console.error('Error al cargar info del usuario:', error);
    }
}

function showChatPage() {
    authPage.classList.remove('active');
    chatPage.classList.add('active');
    loadConversations();
}

// ===== CONVERSACIONES =====

async function loadConversations() {
    try {
        const conversations = await apiRequest('/conversations/');
        renderConversations(conversations);
    } catch (error) {
        showToast('Error al cargar conversaciones', 'error');
    }
}

function renderConversations(conversations) {
    if (conversations.length === 0) {
        conversationsList.innerHTML = `
            <div style="padding: 20px; text-align: center; color: var(--text-secondary);">
                No hay conversaciones aún.<br>
                ¡Crea una nueva!
            </div>
        `;
        return;
    }
    
    conversationsList.innerHTML = conversations.map(conv => `
        <div class="conversation-item ${conv.id === currentConversationId ? 'active' : ''}" 
             data-id="${conv.id}">
            <div class="conversation-title">${conv.title}</div>
            <div class="conversation-meta">
                <span>${conv.message_count || 0} mensajes</span>
                <span>${formatTime(conv.updated_at)}</span>
            </div>
            <button class="conversation-delete" data-id="${conv.id}">×</button>
        </div>
    `).join('');
    
    // Event listeners para conversaciones
    document.querySelectorAll('.conversation-item').forEach(item => {
        item.addEventListener('click', (e) => {
            if (!e.target.classList.contains('conversation-delete')) {
                const convId = parseInt(item.dataset.id);
                loadConversation(convId);
            }
        });
    });
    
    // Event listeners para botones de eliminar
    document.querySelectorAll('.conversation-delete').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const convId = parseInt(btn.dataset.id);
            
            if (confirm('¿Eliminar esta conversación?')) {
                await deleteConversation(convId);
            }
        });
    });
}

async function deleteConversation(convId) {
    try {
        await apiRequest(`/conversations/${convId}`, { method: 'DELETE' });
        
        if (currentConversationId === convId) {
            showWelcomeScreen();
        }
        
        loadConversations();
        showToast('Conversación eliminada', 'success');
    } catch (error) {
        showToast('Error al eliminar conversación', 'error');
    }
}

async function loadConversation(convId) {
    try {
        showLoading();
        const data = await apiRequest(`/chat/history/${convId}`);
        
        currentConversationId = convId;
        renderMessages(data.messages);
        showChatInterface();
        
        // Actualizar UI de conversaciones
        document.querySelectorAll('.conversation-item').forEach(item => {
            item.classList.toggle('active', parseInt(item.dataset.id) === convId);
        });
    } catch (error) {
        showToast('Error al cargar conversación', 'error');
    } finally {
        hideLoading();
    }
}

newChatBtn.addEventListener('click', () => {
    currentConversationId = null;
    showWelcomeScreen();
    showChatInterface();
    messageInput.focus();
});

function showWelcomeScreen() {
    welcomeScreen.style.display = 'flex';
    chatMessages.style.display = 'none';
    chatMessages.innerHTML = '';
    
    document.querySelectorAll('.conversation-item').forEach(item => {
        item.classList.remove('active');
    });
}

function showChatInterface() {
    chatInputContainer.style.display = 'block';
}

// ===== MENSAJES =====

function renderMessages(messages) {
    welcomeScreen.style.display = 'none';
    chatMessages.style.display = 'flex';
    
    chatMessages.innerHTML = messages.map(msg => `
        <div class="message ${msg.role}">
            <div class="message-avatar">
                ${msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div class="message-content">
                <div class="message-text">${escapeHtml(msg.content)}</div>
                <div class="message-time">${formatTime(msg.created_at)}</div>
            </div>
        </div>
    `).join('');
    
    scrollToBottom();
}

function addMessage(role, content, createdAt = new Date().toISOString()) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    messageEl.innerHTML = `
        <div class="message-avatar">
            ${role === 'user' ? '👤' : '🤖'}
        </div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(content)}</div>
            <div class="message-time">${formatTime(createdAt)}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageEl);
    scrollToBottom();
}

function showTypingIndicator() {
    const typingEl = document.createElement('div');
    typingEl.className = 'message assistant';
    typingEl.id = 'typing-indicator';
    typingEl.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingEl);
    scrollToBottom();
}

function hideTypingIndicator() {
    const typingEl = document.getElementById('typing-indicator');
    if (typingEl) {
        typingEl.remove();
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== ENVIAR MENSAJE =====

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Mostrar interfaz de chat si está en welcome screen
    if (welcomeScreen.style.display !== 'none') {
        welcomeScreen.style.display = 'none';
        chatMessages.style.display = 'flex';
    }
    
    // Añadir mensaje del usuario
    addMessage('user', message);
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Deshabilitar input
    sendBtn.disabled = true;
    messageInput.disabled = true;
    
    // Mostrar indicador de escritura
    showTypingIndicator();
    
    try {
        const data = await apiRequest('/chat/', {
            method: 'POST',
            body: JSON.stringify({
                message,
                conversation_id: currentConversationId
            }),
        });
        
        // Actualizar ID de conversación si es nueva
        if (!currentConversationId) {
            currentConversationId = data.conversation_id;
        }
        
        // Ocultar indicador y mostrar respuesta
        hideTypingIndicator();
        addMessage('assistant', data.assistant_message.content, data.assistant_message.created_at);
        
        // Recargar lista de conversaciones
        loadConversations();
        
    } catch (error) {
        hideTypingIndicator();
        showToast(error.message, 'error');
    } finally {
        sendBtn.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
});

// Auto-resize del textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 200) + 'px';
});

// ===== INICIALIZACIÓN =====

window.addEventListener('DOMContentLoaded', async () => {
    if (authToken) {
        try {
            await loadUserInfo();
            showChatPage();
        } catch (error) {
            // Token inválido, limpiar y mostrar login
            localStorage.removeItem('authToken');
            authToken = null;
        }
    }
});
