#!/usr/bin/env python3
"""
Script de prueba para verificar que el API funciona correctamente
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("🧪 Probando AI Chatbot API")
print("=" * 60)

# 1. Verificar health
print("\n1️⃣  Verificando health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Health: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# 2. Verificar root
print("\n2️⃣  Verificando endpoint raíz...")
try:
    response = requests.get(f"{BASE_URL}/")
    data = response.json()
    print(f"✅ Root: {response.status_code}")
    print(f"   Mensaje: {data.get('message')}")
except Exception as e:
    print(f"❌ Error: {e}")

# 3. Intentar registrar un usuario
print("\n3️⃣  Intentando registrar usuario...")
user_data = {
    "username": "testuser123",
    "email": "test@example.com",
    "password": "password123"
}
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json=user_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"✅ Register: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"   Usuario creado: {data.get('username')} ({data.get('email')})")
    else:
        print(f"   Respuesta: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# 4. Intentar login
print("\n4️⃣  Intentando login...")
login_data = {
    "email": "test@example.com",
    "password": "password123"
}
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"✅ Login: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"   Token obtenido: {token[:20]}...")
    else:
        print(f"   Respuesta: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ Prueba completada")
print("=" * 60)
