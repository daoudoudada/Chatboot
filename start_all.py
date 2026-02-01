#!/usr/bin/env python3
"""
Script para iniciar el frontend y backend juntos
Ejecutar con: python start_all.py
"""
import subprocess
import time
import os
from pathlib import Path

os.chdir(Path(__file__).parent)

print("=" * 60)
print("🚀 Iniciando AI Chatbot (Backend + Frontend)")
print("=" * 60)

# Iniciar backend
print("\n📡 Iniciando Backend en puerto 8000...")
backend_process = subprocess.Popen(
    ["python", "run.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

# Esperar a que el backend esté listo
time.sleep(3)

# Iniciar frontend
print("🌐 Iniciando Frontend en puerto 3000...")
frontend_process = subprocess.Popen(
    ["python", "serve_frontend.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

print("\n" + "=" * 60)
print("✅ SERVIDORES INICIADOS:")
print("=" * 60)
print("🌐 Frontend:  http://localhost:3000")
print("📡 Backend:   http://localhost:8000")
print("📚 API Docs:  http://localhost:8000/docs")
print("\n⏹️  Presiona CTRL+C para detener ambos servidores")
print("=" * 60 + "\n")

try:
    # Esperar a que ambos procesos terminen
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    print("\n\n🛑 Deteniendo servidores...")
    backend_process.terminate()
    frontend_process.terminate()
    
    # Esperar a que se detengan
    try:
        backend_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        backend_process.kill()
    
    try:
        frontend_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        frontend_process.kill()
    
    print("✅ Servidores detenidos")
