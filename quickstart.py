#!/usr/bin/env python3
"""
🚀 Quick Start Script para AI Chatbot
Instala todo lo necesario para ejecutar la aplicación
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    """Imprime un header con formato"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def run_command(cmd, description):
    """Ejecuta un comando y maneja errores"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}: OK")
            return True
        else:
            print(f"❌ {description}: ERROR")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print_header("🤖 AI CHATBOT - QUICK START")
    
    # Detectar sistema operativo
    system = platform.system()
    is_windows = system == "Windows"
    
    # Paso 1: Crear venv
    print_header("Paso 1: Creando Virtual Environment")
    
    if is_windows:
        venv_cmd = "python -m venv .venv"
        activate_cmd = ".venv\\Scripts\\activate"
    else:
        venv_cmd = "python3 -m venv .venv"
        activate_cmd = "source .venv/bin/activate"
    
    if not run_command(venv_cmd, "Crear venv"):
        print("❌ No se pudo crear el venv")
        return False
    
    # Paso 2: Instalar dependencias
    print_header("Paso 2: Instalando Dependencias")
    
    if is_windows:
        pip_cmd = ".venv\\Scripts\\pip install -r requirements.txt"
    else:
        pip_cmd = ".venv/bin/pip install -r requirements.txt"
    
    if not run_command(pip_cmd, "Instalar paquetes"):
        print("❌ Error instalando dependencias")
        return False
    
    # Paso 3: Crear .env
    print_header("Paso 3: Configurando Variables de Entorno")
    
    if os.path.exists(".env"):
        print("ℹ️  .env ya existe")
    else:
        try:
            with open(".env", "w") as f:
                f.write("""# AI Chatbot Configuration
OPENAI_API_KEY=sk-proj-TU-CLAVE-AQUI

SECRET_KEY=tu-clave-secreta-cambiar-en-produccion
DATABASE_URL=sqlite:///./ai_chatbot.db
AI_PROVIDER=openai
AI_MODEL=gpt-3.5-turbo
""")
            print("✅ Archivo .env creado")
            print("⚠️  IMPORTANTE: Actualiza tu OPENAI_API_KEY en .env")
        except Exception as e:
            print(f"❌ Error creando .env: {e}")
            return False
    
    # Paso 4: Información final
    print_header("✅ INSTALACIÓN COMPLETADA")
    
    print("""
📝 PRÓXIMOS PASOS:

1. Edita el archivo .env y agrega tu OPENAI_API_KEY
   
2. En TERMINAL 1, inicia el backend:
""")
    
    if is_windows:
        print("   .venv\\Scripts\\activate")
        print("   python run.py")
    else:
        print("   source .venv/bin/activate")
        print("   python run.py")
    
    print("""
3. En TERMINAL 2, inicia el frontend:
""")
    
    if is_windows:
        print("   .venv\\Scripts\\python.exe serve_frontend.py")
    else:
        print("   python serve_frontend.py")
    
    print("""
4. Abre http://localhost:3000 en tu navegador

5. ¡Regístrate y comienza a chatear!

📚 Ver README.md para más información.
""")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
