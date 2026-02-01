import sqlite3
from pathlib import Path

db_path = Path('ai_chatbot.db')
if db_path.exists():
    print(f'✅ Base de datos existe: {db_path.stat().st_size} bytes')
    conn = sqlite3.connect('ai_chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    print(f'Tablas en BD: {tables}')
    
    # Ver estructura de tabla users
    if any('users' in table for table in tables):
        cursor.execute('PRAGMA table_info(users)')
        columns = cursor.fetchall()
        print('\nEstructura tabla users:')
        for col in columns:
            print(f'  - {col[1]}: {col[2]}')
    
    conn.close()
else:
    print('❌ Base de datos NO existe')
