# 🤖 AI Chatbot - Full Stack Application

> Una aplicación de chat inteligente con integración de IA (OpenAI/Gemini) construida con FastAPI, SQLAlchemy y JavaScript vanilla.

[![Python 3.14+](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Tabla de Contenidos

- [Features](#-features)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Troubleshooting](#-troubleshooting)
- [Contribución](#-contribución)

## ✨ Features

- ✅ **Autenticación JWT** - Registro y login seguros con tokens JWT
- ✅ **Chat en Tiempo Real** - Interfaz intuitiva para chatear con IA
- ✅ **Múltiples Proveedores de IA** - Soporta OpenAI (ChatGPT) y Google Gemini
- ✅ **Historial de Conversaciones** - Guarda y recupera conversaciones anteriores
- ✅ **Hash de Contraseñas** - Contraseñas hasheadas con Argon2 (seguro)
- ✅ **CORS Habilitado** - Comunicación frontend-backend sin problemas
- ✅ **API REST Completa** - Endpoints bien estructurados y documentados
- ✅ **Base de Datos SQLite** - Persistencia de datos en local
- ✅ **Interfaz Web Moderna** - HTML5, CSS3 y JavaScript vanilla

## 🔧 Requisitos

- **Python 3.14+**
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)
- **Clave API de OpenAI o Google Gemini**

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/daoudoudada/ai-chatbot-app.git
cd ai-chatbot-app
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-tu-clave-aqui

# O para Gemini
GEMINI_API_KEY=tu-clave-gemini-aqui

# Configuración opcional
SECRET_KEY=tu-clave-secreta-muy-segura
DATABASE_URL=sqlite:///./ai_chatbot.db
```

> ⚠️ **Importante**: Nunca commits el archivo `.env` con claves reales. Usa `.env.example` en el repo.

## 🚀 Uso

### 1. Iniciar el Backend (FastAPI)

```bash
# Opción 1: Desde Python
python run.py

# Opción 2: Directamente con uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

**Documentación de API (Swagger)**: `http://localhost:8000/docs`

### 2. Iniciar el Frontend (en otra terminal)

```bash
# Windows
.venv\Scripts\python.exe serve_frontend.py

# macOS/Linux
python serve_frontend.py
```

El frontend estará disponible en: `http://localhost:3000`

### 3. Acceder a la aplicación

1. Abre tu navegador en `http://localhost:3000`
2. **Regístrate** con un email y contraseña
3. **Inicia sesión** con tus credenciales
4. **Comienza a chatear** con la IA

## 📡 API Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/register` | Registrar nuevo usuario |
| POST | `/api/auth/login` | Iniciar sesión |
| GET | `/api/auth/me` | Obtener perfil del usuario actual |

#### Ejemplo: Registro

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

#### Ejemplo: Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

### Conversaciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/conversations` | Crear nueva conversación |
| GET | `/api/conversations` | Obtener todas las conversaciones del usuario |
| GET | `/api/conversations/{id}` | Obtener una conversación específica |

### Chat

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/chat/send-message` | Enviar mensaje y obtener respuesta de IA |

#### Ejemplo: Enviar mensaje

```bash
curl -X POST "http://localhost:8000/api/chat/send-message" \
  -H "Authorization: Bearer {tu_jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 1,
    "content": "Hola, cual es la capital de Francia?"
  }'
```

### Salud

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check del servidor |

## 📁 Estructura del Proyecto

```
ai-chatbot-app/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada FastAPI
│   ├── auth.py                 # Utilidades de autenticación
│   ├── config.py               # Configuración de la app
│   ├── database.py             # Conexión a BD
│   ├── models.py               # Modelos SQLAlchemy
│   ├── schemas.py              # Schemas Pydantic
│   ├── ai_service.py           # Integración con IA
│   ├── routes/
│   │   ├── auth.py             # Endpoints de autenticación
│   │   ├── chat.py             # Endpoints de chat
│   │   └── conversations.py    # Endpoints de conversaciones
│   └── tests/
│       └── test_api.py
│
├── frontend/
│   ├── index.html              # Página principal
│   ├── styles.css              # Estilos
│   └── app.js                  # Lógica JavaScript
│
├── database/
│   └── schema.sql              # Schema SQL
│
├── docs/
│   ├── CUSTOMIZATION.md        # Guía de personalización
│   ├── DEPLOYMENT.md           # Guía de despliegue
│   └── EXTRA_FEATURES.md       # Características adicionales
│
├── .env.example                # Plantilla de variables de entorno
├── requirements.txt            # Dependencias de Python
├── run.py                      # Script para iniciar el backend
├── serve_frontend.py           # Script para servir el frontend
└── README.md                   # Este archivo
```

## 🔐 Configuración de Seguridad

### Contraseñas

Las contraseñas se hashean con **Argon2**, un algoritmo seguro y moderno:

```python
from backend.auth import get_password_hash, verify_password

# Hashear contraseña
hashed = get_password_hash("mi_contraseña")

# Verificar contraseña
if verify_password("mi_contraseña", hashed):
    print("¡Contraseña correcta!")
```

### JWT Tokens

Los tokens JWT se generan con:
- **Algoritmo**: HS256
- **Expiración**: 30 minutos (configurable)
- **Clave secreta**: Definida en `.env`

### CORS

Configurado para aceptar solicitudes desde `http://localhost:3000` en desarrollo.

Para producción, actualiza en `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],  # Cambiar aquí
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🐛 Troubleshooting

### Error: "No module named 'fastapi'"

```bash
pip install -r requirements.txt
```

### Error: "OPENAI_API_KEY no configurada"

Asegúrate de:
1. Crear archivo `.env` en la raíz
2. Agregar tu clave: `OPENAI_API_KEY=sk-proj-...`
3. Reiniciar el servidor

### Puerto 8000 ya está en uso

```bash
# Matar proceso en puerto 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID {PID} /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### "Cannot connect to database"

Asegúrate de que tienes permisos de escritura en la carpeta del proyecto:

```bash
# Windows
icacls "C:\path\to\ai-chatbot-app" /grant:r "%USERNAME%":F

# macOS/Linux
chmod -R 755 /path/to/ai-chatbot-app
```

## 📈 Rendimiento

- **Backend**: Uvicorn con reload automático en desarrollo
- **Frontend**: Servido con Python http.server (puede ser mejorado con nginx en producción)
- **Base de Datos**: SQLite (cambiar a PostgreSQL para producción)

## 🚀 Despliegue a Producción

Ver [DEPLOYMENT.md](docs/DEPLOYMENT.md) para instrucciones detalladas sobre cómo desplegar a:
- Heroku
- AWS
- DigitalOcean
- Railway

## 🎨 Personalización

Ver [CUSTOMIZATION.md](docs/CUSTOMIZATION.md) para:
- Cambiar tema/colores
- Agregar nuevos campos de usuario
- Integrar nuevos proveedores de IA
- Modificar prompts del sistema

## 📚 Características Adicionales

Ver [EXTRA_FEATURES.md](docs/EXTRA_FEATURES.md) para:
- Exportar conversaciones
- Buscar en historial
- Compartir conversaciones
- Soporte para múltiples idiomas

## 🤝 Contribución

¡Las contribuciones son bienvenidas!

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Pasos para desarrollo

```bash
# 1. Instalar en modo desarrollo
pip install -r requirements.txt

# 2. Crear rama
git checkout -b mi-feature

# 3. Hacer cambios y testear
python run.py

# 4. Commit y push
git add .
git commit -m "Descripción clara del cambio"
git push origin mi-feature
```

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/daoudoudada/ai-chatbot-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/daoudoudada/ai-chatbot-app/discussions)
- **Email**: oudadadaoud21@gmail.com

## 🌟 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [OpenAI](https://openai.com/)
- [Google Gemini](https://ai.google.dev/)

---

<div align="center">

**[⬆ Volver al inicio](#-ai-chatbot---full-stack-application)**

Hecho con ❤️ por [Daoud Oudada](https://www.linkedin.com/in/daoud-oudada/)

**Email**: oudadadaoud21@gmail.com | **LinkedIn**: [Daoud Oudada](https://www.linkedin.com/in/daoud-oudada/)

</div>
