"""
Tests básicos para la API
Ejecutar con: pytest backend/tests/test_api.py
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import get_db, Base, engine

# Cliente de test
client = TestClient(app)

# Setup de base de datos de test
@pytest.fixture(autouse=True)
def setup_database():
    """Crea tablas antes de cada test y las elimina después"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestAuth:
    """Tests de autenticación"""
    
    def test_register_user(self):
        """Test: Registrar un nuevo usuario"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "id" in data
    
    def test_register_duplicate_email(self):
        """Test: No permitir emails duplicados"""
        # Primer registro
        client.post(
            "/api/auth/register",
            json={
                "username": "user1",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        # Segundo registro con mismo email
        response = client.post(
            "/api/auth/register",
            json={
                "username": "user2",
                "email": "test@example.com",
                "password": "password456"
            }
        )
        assert response.status_code == 400
        assert "ya está registrado" in response.json()["detail"]
    
    def test_login_success(self):
        """Test: Login exitoso"""
        # Registrar usuario
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self):
        """Test: Login con contraseña incorrecta"""
        # Registrar usuario
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        # Login con contraseña incorrecta
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401


class TestConversations:
    """Tests de conversaciones"""
    
    @pytest.fixture
    def auth_token(self):
        """Crea un usuario y devuelve su token"""
        # Registrar
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        return response.json()["access_token"]
    
    def test_create_conversation(self, auth_token):
        """Test: Crear conversación"""
        response = client.post(
            "/api/conversations/",
            json={"title": "Test Conversation"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Conversation"
        assert "id" in data
    
    def test_list_conversations(self, auth_token):
        """Test: Listar conversaciones"""
        # Crear algunas conversaciones
        for i in range(3):
            client.post(
                "/api/conversations/",
                json={"title": f"Conversation {i}"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )
        
        # Listar
        response = client.get(
            "/api/conversations/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def test_unauthorized_access(self):
        """Test: Acceso sin token"""
        response = client.get("/api/conversations/")
        assert response.status_code == 401


class TestHealth:
    """Tests de endpoints básicos"""
    
    def test_root_endpoint(self):
        """Test: Endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    def test_health_check(self):
        """Test: Health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


# Para ejecutar tests:
# pip install pytest
# pytest backend/tests/test_api.py -v
