@echo off
REM Script para iniciar Backend y Frontend en Windows
REM Mantiene ambas ventanas abiertas

cd /d "%~dp0"

echo ============================================================
echo Iniciando AI Chatbot (Backend + Frontend)
echo ============================================================

REM Iniciar Backend en una nueva ventana
start "Backend - Chatbot" cmd /k python run.py

REM Esperar 3 segundos
timeout /t 3 /nobreak

REM Iniciar Frontend en otra ventana
start "Frontend - Chatbot" cmd /k python serve_frontend.py

echo.
echo ============================================================
echo SERVIDORES INICIADOS:
echo ============================================================
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo ============================================================
echo.
