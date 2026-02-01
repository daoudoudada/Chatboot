#!/usr/bin/env python3
"""
Script para ejecutar el servidor FastAPI
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando servidor AI Chatbot...")
    print("📝 API Docs: http://localhost:8000/docs")
    print("🌐 Frontend: Abre frontend/index.html en tu navegador")
    print("\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
