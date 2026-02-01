#!/usr/bin/env python3
"""
Servidor simple para servir el frontend
Ejecutar con: python serve_frontend.py
Abre: http://localhost:3000
"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
FRONTEND_DIR = Path(__file__).parent / "frontend"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)
    
    def end_headers(self):
        # Agregar headers para prevenir caching y CORS
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

print(f"🌐 Sirviendo frontend desde {FRONTEND_DIR}")
print(f"📂 Puerto: {PORT}")
print(f"🔗 Abre: http://localhost:{PORT}")
print(f"⚙️  Backend: http://localhost:8000")
print("\nPresiona CTRL+C para detener")

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Servidor detenido")
