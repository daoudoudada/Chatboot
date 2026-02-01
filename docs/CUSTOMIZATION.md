# 🎨 Guía de Personalización

Esta guía te muestra cómo personalizar el chatbot para que se adapte a tus necesidades.

## 🤖 Personalizar el Comportamiento del Bot

### Opción 1: Editar archivo de configuración

Edita `backend/config.py`:

```python
SYSTEM_PROMPT: str = """
Aquí defines la personalidad y expertise de tu bot.

Ejemplos de prompts:

1. ASISTENTE DE MARKETING:
Eres un experto en marketing digital y redes sociales.
Ayudas a crear estrategias de contenido, analizar métricas
y optimizar campañas publicitarias. Siempre proporciona
ejemplos prácticos y datos actualizados.

2. COACH DE FITNESS:
Eres un entrenador personal certificado y nutricionista.
Creas planes de entrenamiento personalizados, diseñas
dietas balanceadas y motivas a las personas a alcanzar
sus objetivos de salud.

3. TUTOR DE PROGRAMACIÓN:
Eres un desarrollador senior con 10 años de experiencia.
Enseñas programación desde cero, explicas conceptos
complejos de forma simple y proporcionas código de
ejemplo bien comentado.

4. ASISTENTE FINANCIERO:
Eres un asesor financiero especializado en finanzas
personales. Ayudas a crear presupuestos, planificar
inversiones y entender conceptos económicos.
"""
```

### Opción 2: Usar variables de entorno

Edita `.env`:

```env
SYSTEM_PROMPT=Eres un asistente experto en [TU ESPECIALIDAD]. Tu objetivo es [LO QUE HACE]. Siempre [ESTILO DE COMUNICACIÓN].
```

## 🎨 Personalizar la Apariencia

### Cambiar colores

Edita `frontend/styles.css` (líneas 1-15):

```css
:root {
    /* Color principal (botones, enlaces) */
    --primary-color: #10a37f;     /* Verde → Cambiar por tu color */
    --primary-dark: #0d8c6d;
    
    /* Colores de fondo */
    --background: #ffffff;         /* Blanco */
    --surface: #f7f7f8;           /* Gris claro */
    
    /* Colores de texto */
    --text-primary: #2d2d2d;      /* Negro suave */
    --text-secondary: #6e6e80;    /* Gris */
}
```

**Paletas de colores sugeridas:**

**Azul profesional:**
```css
--primary-color: #2563eb;
--primary-dark: #1d4ed8;
```

**Morado moderno:**
```css
--primary-color: #7c3aed;
--primary-dark: #6d28d9;
```

**Rojo enérgico:**
```css
--primary-color: #dc2626;
--primary-dark: #b91c1c;
```

### Cambiar el título y emojis

Edita `frontend/index.html`:

```html
<!-- Línea 5 -->
<title>Tu Título Aquí</title>

<!-- Línea 14 -->
<h1>🎯 Tu Nombre de App</h1>
<p>Tu descripción aquí</p>

<!-- Líneas 71-93 - Features -->
<div class="feature">
    <span class="feature-icon">🎨</span>
    <h3>Tu Feature 1</h3>
    <p>Descripción</p>
</div>
```

### Cambiar avatares de mensajes

Edita `frontend/app.js` (busca emojis):

```javascript
// Usuario (línea ~335 aprox)
${msg.role === 'user' ? '👤' : '🤖'}

// Puedes cambiar a:
${msg.role === 'user' ? '😊' : '🎯'}
${msg.role === 'user' ? '💼' : '📊'}
${msg.role === 'user' ? '🧑‍💻' : '🤖'}
```

## 🤖 Cambiar el Modelo de IA

### Usar modelos diferentes

Edita `.env`:

```env
# OpenAI - Modelos disponibles:
AI_MODEL=gpt-3.5-turbo      # Rápido y económico
AI_MODEL=gpt-4              # Más inteligente
AI_MODEL=gpt-4-turbo        # Último modelo

# Gemini - Modelos disponibles:
AI_MODEL=gemini-pro         # Modelo estándar
AI_MODEL=gemini-pro-vision  # Con capacidad de imágenes
```

### Ajustar parámetros de generación

Edita `backend/ai_service.py`:

```python
# Para OpenAI (línea ~47 aprox)
"temperature": 0.7,      # 0.0 = Conservador, 1.0 = Creativo
"max_tokens": 1000,      # Longitud máxima de respuesta

# Para Gemini (línea ~77 aprox)
"temperature": 0.7,
"maxOutputTokens": 1000,
```

## 📊 Cambiar Base de Datos

### De SQLite a PostgreSQL

1. Instala PostgreSQL

2. Crea la base de datos:
```bash
psql -U postgres
CREATE DATABASE mi_chatbot;
\q
```

3. Actualiza `.env`:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/mi_chatbot
```

4. Reinicia el servidor (las tablas se crean automáticamente)

## 🔐 Mejorar la Seguridad

### Cambiar configuración JWT

Edita `.env`:

```env
# Genera una clave segura (Linux/Mac):
# python -c "import secrets; print(secrets.token_urlsafe(32))"

SECRET_KEY=tu-clave-super-segura-generada

# Tiempo de expiración del token (en minutos)
ACCESS_TOKEN_EXPIRE_MINUTES=60  # 1 hora (default: 30)
```

## 📱 Personalizar Mensajes de la UI

### Mensajes de bienvenida

Edita `frontend/index.html`:

```html
<!-- Líneas 71-95 - Welcome Screen -->
<h1>🤖 Tu Mensaje de Bienvenida</h1>
<p>Tu subtítulo o descripción</p>
```

### Textos de formularios

```html
<!-- Placeholders -->
<input placeholder="tu-nuevo-placeholder">

<!-- Labels -->
<label>Tu nuevo label</label>

<!-- Botones -->
<button>Tu nuevo texto</button>
```

## 🌐 Personalizar API URLs

### Cambiar puerto del backend

Edita `run.py`:

```python
uvicorn.run(
    "backend.main:app",
    host="0.0.0.0",
    port=8080,  # Cambiar aquí
    reload=True
)
```

### Cambiar URL del frontend

Edita `frontend/app.js`:

```javascript
// Línea 2
const API_URL = 'http://localhost:8080/api';  // Actualizar puerto
```

## 🎯 Casos de Uso Específicos

### 1. Bot de Atención al Cliente

```python
SYSTEM_PROMPT = """
Eres un asistente de atención al cliente de [EMPRESA].
Respondes de forma amable, profesional y eficiente.
Conoces los productos: [LISTA].
Políticas: [POLÍTICAS].
Horario de atención: [HORARIO].
"""
```

### 2. Asistente Educativo

```python
SYSTEM_PROMPT = """
Eres un tutor educativo especializado en [MATERIA].
Nivel: [PRIMARIA/SECUNDARIA/UNIVERSIDAD].
Explicas conceptos complejos de forma simple.
Usas ejemplos del día a día.
Eres paciente y motivador.
"""
```

### 3. Consultor Técnico

```python
SYSTEM_PROMPT = """
Eres un consultor técnico experto en [TECNOLOGÍA].
Stack: [LISTA DE TECNOLOGÍAS].
Proporcionas soluciones prácticas.
Código de ejemplo bien documentado.
Best practices y patrones de diseño.
"""
```

## 📝 Tips de Personalización

1. **Sé específico**: Define claramente qué debe hacer el bot
2. **Da contexto**: Incluye información relevante en el prompt
3. **Define el tono**: Formal, casual, técnico, divertido, etc.
4. **Establece límites**: Qué NO debe hacer el bot
5. **Prueba iterativamente**: Ajusta el prompt según resultados

## 🔄 Actualizar después de cambios

Después de modificar archivos:

1. **Backend**: Reinicia el servidor (Ctrl+C y `python run.py`)
2. **Frontend**: Recarga el navegador (F5)
3. **.env**: Siempre reiniciar el servidor

## 📚 Recursos Adicionales

- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Gemini Prompting Guide](https://ai.google.dev/docs/prompt_best_practices)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

---

¿Necesitas más ayuda? Consulta el [README.md](README.md) principal.
