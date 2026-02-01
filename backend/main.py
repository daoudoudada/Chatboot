"""
Aplicación principal FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Crear aplicación PRIMERO
app = FastAPI(
    title="AI Chatbot API",
    description="API REST para chatbot con inteligencia artificial",
    version="1.0.0"
)

# Agregar CORS middleware ANTES de todo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar después de crear la app
from .database import init_db
from .routes import auth, conversations, chat

# Endpoints raíz ANTES de los routers
@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "AI Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Incluir routers DESPUÉS
app.include_router(auth.router, prefix="/api")
app.include_router(conversations.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    init_db()
    print("[OK] Base de datos inicializada")
    print("[INFO] Servidor iniciado correctamente")
    print("[INFO] CORS habilitado para http://localhost:3000")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
