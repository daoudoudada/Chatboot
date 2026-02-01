# 🚀 Guía de Despliegue

Esta guía te muestra cómo llevar tu chatbot a producción.

## 📋 Pre-requisitos de Producción

Antes de desplegar, asegúrate de:

- ✅ Tener una API key válida (OpenAI o Gemini)
- ✅ Configurar PostgreSQL (recomendado para producción)
- ✅ Generar una `SECRET_KEY` segura
- ✅ Configurar variables de entorno
- ✅ Probar localmente

## 🌐 Opción 1: Railway (Recomendado - Fácil)

Railway es perfecto para principiantes. Deploy en minutos.

### Backend

1. **Crear cuenta en [Railway.app](https://railway.app/)**

2. **Crear nuevo proyecto**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"

3. **Conectar repositorio**
   - Autoriza Railway a acceder a tu GitHub
   - Selecciona tu repositorio

4. **Configurar variables de entorno**
   ```env
   SECRET_KEY=genera-una-clave-segura-aqui
   AI_PROVIDER=openai
   OPENAI_API_KEY=tu-api-key
   DATABASE_URL=${RAILWAY_DATABASE_URL}  # Railway lo provee automáticamente
   ```

5. **Añadir PostgreSQL**
   - Click en "+ New"
   - Selecciona "Database" → "PostgreSQL"
   - Railway conecta automáticamente

6. **Deploy automático**
   - Railway detecta Python y FastAPI
   - Deploy automático en cada push a main

### Frontend

1. **Actualizar API URL**
   
   En `frontend/app.js`:
   ```javascript
   const API_URL = 'https://tu-app.railway.app/api';
   ```

2. **Deploy en Vercel/Netlify** (ver más abajo)

## 🎨 Opción 2: Render

Similar a Railway, gratuito con limitaciones.

### Backend

1. **Crear cuenta en [Render.com](https://render.com/)**

2. **Nuevo Web Service**
   - "New +" → "Web Service"
   - Conecta GitHub
   - Selecciona repositorio

3. **Configuración**
   ```
   Name: ai-chatbot-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Variables de entorno**
   - Añade las mismas que en Railway

5. **PostgreSQL**
   - "New +" → "PostgreSQL"
   - Copia la "Internal Database URL"
   - Añade como `DATABASE_URL` en variables

## ☁️ Opción 3: Vercel (Solo Frontend)

Para el frontend estático.

1. **Instalar Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

3. **Configurar**
   - Acepta configuración default
   - En `app.js`, actualiza `API_URL` con tu backend

## 🌟 Opción 4: Netlify (Solo Frontend)

1. **Arrastrar y soltar**
   - Ve a [Netlify.com](https://netlify.com)
   - Arrastra la carpeta `frontend/`
   - ¡Listo!

2. **O con Git**
   - Conecta repositorio
   - Build settings: None (es estático)
   - Publish directory: `frontend/`

## 🐳 Opción 5: Docker (Avanzado)

### Crear Dockerfile

Crea `Dockerfile` en la raíz:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Crear docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/chatbot
    depends_on:
      - db
    env_file:
      - .env

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: chatbot
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Deploy

```bash
docker-compose up -d
```

## ⚙️ Configuración de Producción

### 1. SECRET_KEY Segura

Genera una clave única:

```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copia el resultado a `.env`:
```env
SECRET_KEY=el-resultado-aqui
```

### 2. CORS en Producción

Edita `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tu-frontend.vercel.app",  # Tu frontend
        "https://tu-dominio.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. PostgreSQL en Producción

No uses SQLite en producción. Configura PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@host:5432/database
```

Railway y Render proveen PostgreSQL automáticamente.

### 4. HTTPS

Todos los servicios mencionados (Railway, Render, Vercel, Netlify) 
proveen HTTPS automáticamente. ✅

## 🔒 Checklist de Seguridad

Antes de hacer público tu chatbot:

- [ ] `SECRET_KEY` única y segura
- [ ] Variables de entorno configuradas
- [ ] API Keys seguras (no en el código)
- [ ] CORS configurado correctamente
- [ ] PostgreSQL en lugar de SQLite
- [ ] HTTPS habilitado
- [ ] Logs monitoreados
- [ ] Rate limiting (opcional)

## 📊 Monitoreo

### Logs en Railway
- Dashboard → Tu proyecto → "Logs"
- Ver requests, errores, etc.

### Logs en Render
- Dashboard → Tu servicio → "Logs"

### Healthcheck

Configura monitoring:
```
https://tu-api.com/health
```

Servicios como [UptimeRobot](https://uptimerobot.com/) son gratuitos.

## 💰 Costos Estimados

### Free Tier
- **Railway**: $5 de crédito inicial, luego ~$5/mes
- **Render**: Gratis con limitaciones
- **Vercel**: Gratis para proyectos personales
- **Netlify**: Gratis (100GB/mes)

### APIs de IA
- **OpenAI GPT-3.5**: ~$0.002 / 1K tokens
- **OpenAI GPT-4**: ~$0.03 / 1K tokens
- **Gemini**: Gratis hasta cierto límite

**Ejemplo**: 1000 mensajes/mes con GPT-3.5 ≈ $1-2

## 🔄 CI/CD Automático

Con GitHub, cada push a `main` despliega automáticamente en:
- Railway ✅
- Render ✅
- Vercel ✅
- Netlify ✅

## 🌍 Dominio Personalizado

### En Railway/Render
1. Settings → Domains
2. Añade tu dominio
3. Configura DNS (CNAME)

### En Vercel/Netlify
1. Project Settings → Domains
2. Add Custom Domain
3. Sigue instrucciones DNS

## 📈 Escalabilidad

Para muchos usuarios:

1. **Usar PostgreSQL** (no SQLite)
2. **Habilitar pooling** en la DB
3. **Cachear respuestas** comunes
4. **Load balancing** (Railway/Render lo hacen automático)
5. **CDN** para frontend (Vercel/Netlify incluido)

## 🆘 Troubleshooting

### "Application failed to respond"
→ Verifica el comando de inicio:
```
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### "Module not found"
→ Asegúrate que `requirements.txt` está en la raíz

### "Database connection failed"
→ Verifica `DATABASE_URL` en variables de entorno

### "API Key error"
→ Verifica que `OPENAI_API_KEY` o `GEMINI_API_KEY` está configurada

## 📚 Recursos

- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Netlify Docs](https://docs.netlify.com/)

## ✅ Checklist Final

Antes de ir a producción:

- [ ] Backend deployado y funcionando
- [ ] Frontend deployado y funcionando
- [ ] Base de datos PostgreSQL configurada
- [ ] Variables de entorno seguras
- [ ] CORS configurado
- [ ] API Keys válidas
- [ ] Dominio personalizado (opcional)
- [ ] Monitoring configurado
- [ ] Probado en producción

---

**¡Felicidades!** 🎉 Tu chatbot está en producción.

¿Problemas? Abre un issue en GitHub.
