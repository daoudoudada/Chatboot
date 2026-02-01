# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al AI Chatbot! 

## 🚀 Cómo Contribuir

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU-USUARIO/ai-chatbot.git
cd ai-chatbot
```

### 2. Crear Rama

```bash
git checkout -b feature/mi-nueva-caracteristica
```

### 3. Hacer Cambios

- Escribe código limpio y comentado
- Sigue las convenciones de estilo
- Prueba tus cambios

### 4. Commit

```bash
git add .
git commit -m "feat: añade [descripción breve]"
```

**Convención de commits:**
- `feat:` Nueva característica
- `fix:` Corrección de bug
- `docs:` Documentación
- `style:` Formato/estilo
- `refactor:` Refactorización
- `test:` Tests
- `chore:` Mantenimiento

### 5. Push y Pull Request

```bash
git push origin feature/mi-nueva-caracteristica
```

Luego crea un Pull Request en GitHub.

## 📋 Estándares de Código

### Python (Backend)

```python
# Usar type hints
def funcion(parametro: str) -> int:
    """Docstring describiendo la función"""
    return len(parametro)

# Nombres descriptivos
user_id = 123  # ✅
x = 123        # ❌

# Seguir PEP 8
```

### JavaScript (Frontend)

```javascript
// Usar const/let, no var
const API_URL = 'http://localhost:8000';  // ✅
var url = 'http://localhost:8000';        // ❌

// Nombres en camelCase
const userId = 123;     // ✅
const user_id = 123;    // ❌

// Comentarios claros
// Obtener token de autenticación
const token = localStorage.getItem('authToken');
```

## ✅ Checklist antes de PR

- [ ] Código funciona correctamente
- [ ] Código está comentado
- [ ] Documentación actualizada
- [ ] Tests pasan (si aplica)
- [ ] Sin errores de lint
- [ ] Commit messages claros

## 🐛 Reportar Bugs

Usa GitHub Issues con:
- **Título claro**: "Error al enviar mensaje con emojis"
- **Descripción**: Qué esperabas vs. qué pasó
- **Pasos para reproducir**: Lista numerada
- **Capturas de pantalla**: Si aplica
- **Entorno**: OS, navegador, versión

## 💡 Sugerir Features

GitHub Issues con:
- **Título**: "Feature: [nombre]"
- **Descripción**: Qué problema resuelve
- **Casos de uso**: Ejemplos reales
- **Mockups**: Si es UI (opcional)

## 📚 Áreas de Contribución

- 🐛 **Bug fixes**: Corregir errores
- ✨ **Features**: Nuevas características
- 📝 **Documentación**: Mejorar docs
- 🎨 **UI/UX**: Diseño y experiencia
- 🧪 **Tests**: Añadir pruebas
- 🌍 **Traducciones**: i18n

## 🎯 Prioridades Actuales

1. Mejorar tests
2. Dark mode
3. Exportar conversaciones
4. Búsqueda avanzada
5. Mejoras de UI/UX

## ❓ Preguntas

Si tienes dudas, abre un Issue o contacta al mantenedor.

## 📜 Código de Conducta

- Sé respetuoso y profesional
- Acepta críticas constructivas
- Ayuda a otros contributors
- Reporta comportamiento inapropiado

---

¡Gracias por hacer este proyecto mejor! 🚀
