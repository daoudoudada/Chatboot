import sys
import traceback
from backend.database import engine, init_db
from backend.models import Base, User
from backend.schemas import UserCreate
from backend.auth import get_password_hash
from sqlalchemy.orm import sessionmaker

# Inicializar BD
print("🔍 Probando registro manualmente...")

try:
    init_db()
    print("✅ BD inicializada")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Crear usuario de test
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    print(f"📝 Creando usuario: {user_data.username} ({user_data.email})")
    
    # Verificar si existe
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        print("❌ El email ya existe")
        db.query(User).filter(User.email == user_data.email).delete()
        db.commit()
        print("✅ Usuario anterior eliminado")
    
    # Crear nuevo usuario
    hashed_pwd = get_password_hash(user_data.password)
    print(f"🔐 Password hasheado: {hashed_pwd[:50]}...")
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pwd
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"✅ Usuario creado: ID={new_user.id}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
finally:
    if 'db' in locals():
        db.close()
