import requests
import json
import time

time.sleep(2)

data = {
    'username': f'user_{int(time.time())}',
    'email': f'test_{int(time.time())}@test.com',
    'password': 'SecurePassword123!'
}

print('🧪 Probando registro...')
try:
    response = requests.post(
        'http://localhost:8000/api/auth/register',
        json=data,
        timeout=10
    )
    print(f'Status: {response.status_code}')
    
    if response.status_code == 201:
        print('✅ ¡REGISTRO EXITOSO!')
        result = response.json()
        print(f'Usuario: {result.get("username")} (ID: {result.get("id")})')
    else:
        print(f'Error: {response.text[:200]}')
        
except Exception as e:
    print(f'Error: {e}')
