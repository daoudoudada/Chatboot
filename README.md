# 🤖 AI Chatbot - Full Stack Application

Aplicación **full stack** de chat con IA: backend en **FastAPI** y frontend en **HTML/CSS/JS**. Incluye **registro/login con JWT**, historial de conversaciones y soporte para **OpenAI** o **Google Gemini** como proveedor de IA.

## Qué puedes hacer
- Crear cuenta e iniciar sesión (**JWT**)
- Chatear con la IA desde una interfaz web
- Guardar y consultar **conversaciones** (historial)
- Cambiar proveedor de IA (OpenAI / Gemini) usando variables de entorno

## Stack
- **Backend:** Python + FastAPI
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Base de datos:** SQLite (con SQLAlchemy)
- **Auth:** JWT + contraseñas hasheadas con **Argon2**

## Estructura del proyecto
```text
Chatboot/
├── backend/                 # API FastAPI
│   ├── main.py
│   ├── routes/              # auth, chat, conversations...
│   ├── models.py
│   └── ...
├── frontend/                # UI web (html/css/js)
├── database/                # schema.sql
├── docs/                    # guías extra (deploy, customization...)
├── run.py                   # arranque backend
├── serve_frontend.py        # servidor simple para el frontend
├── requirements.txt
└── README.md
```

## Requisitos
- Python **3.14+**
- Una API key de **OpenAI** o **Gemini**

## Instalación
1) Clonar el repo:
```bash
git clone https://github.com/daoudoudada/Chatboot.git
cd Chatboot
```

2) Entorno virtual e instalación:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuración (.env)
Crea un archivo `.env` en la raíz (puedes partir de `.env.example` si existe):

```env
# OpenAI
OPENAI_API_KEY=tu_clave

# o Gemini
GEMINI_API_KEY=tu_clave

# Backend
SECRET_KEY=una_clave_larga_y_segura
DATABASE_URL=sqlite:///./ai_chatbot.db
```

## Ejecutar
### 1) Backend (FastAPI)
```bash
python run.py
# o
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

### 2) Frontend
En otra terminal:
```bash
# Windows (si lo tienes así en el proyecto)
.venv\Scripts\python.exe serve_frontend.py
# macOS/Linux
python serve_frontend.py
```

Frontend: `http://localhost:3000`

## Endpoints principales (resumen)
- Auth:
  - `POST /api/auth/register`
  - `POST /api/auth/login`
  - `GET /api/auth/me`
- Conversaciones:
  - `POST /api/conversations`
  - `GET /api/conversations`
  - `GET /api/conversations/{id}`
- Chat:
  - `POST /api/chat/send-message`
- Health:
  - `GET /health`

## Notas rápidas
- Si no responde la IA, revisa que tengas `OPENAI_API_KEY` o `GEMINI_API_KEY` configurada y reinicia el backend.
- Si cambias puertos/orígenes, ajusta CORS en el backend.
