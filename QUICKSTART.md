# 🚀 Guía de Inicio Rápido

## Instalación en 5 minutos

### 1️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar API Key

Crea un archivo `.env`:

```bash
cp .env.example .env
```

Edita `.env` y añade tu API key:

**Para OpenAI:**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-tu-key-aqui
```

**Para Gemini:**
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=tu-key-aqui
```

### 3️⃣ Iniciar servidor

```bash
python run.py
```

### 4️⃣ Abrir aplicación

Abre `frontend/index.html` en tu navegador.

## 🎯 Primeros pasos

1. **Registrarse**: Crea una cuenta con email y contraseña
2. **Login**: Inicia sesión
3. **Chat**: Haz clic en el botón "+" y empieza a chatear

## 📌 URLs importantes

- **Frontend**: `frontend/index.html`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

## 🔑 Obtener API Keys

### OpenAI (ChatGPT)
1. Ir a [platform.openai.com](https://platform.openai.com/)
2. Crear cuenta
3. Ir a "API Keys"
4. Crear nueva key
5. Copiar y pegar en `.env`

### Google Gemini
1. Ir a [ai.google.dev](https://ai.google.dev/)
2. Crear cuenta
3. "Get API Key"
4. Crear nueva key
5. Copiar y pegar en `.env`

## ⚡ Personalizar el bot

Edita `backend/config.py` o `.env`:

```python
SYSTEM_PROMPT = """
Eres un experto en [TU TEMA AQUÍ].
Ayudas a los usuarios a [LO QUE HACE TU BOT].
"""
```

## 🐛 Problemas comunes

**Error: "OPENAI_API_KEY no configurada"**
→ Verifica que `.env` existe y tiene la API key

**Error: "Module not found"**
→ Ejecuta: `pip install -r requirements.txt`

**Error: "Port already in use"**
→ Cambia el puerto en `run.py`: `port=8001`

## 📚 Más información

Lee el [README.md](README.md) completo para documentación detallada.

---

¿Listo? **¡A chatear con IA!** 🤖
