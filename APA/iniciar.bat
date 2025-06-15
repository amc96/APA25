@echo off
echo ======================================
echo Instalando dependencias necessarias...
echo ======================================
pip install pandas numpy matplotlib flask

echo.
echo ===================================================
echo Iniciando aplicacao web de conversao CSV para Matriz
echo ===================================================
python app.py

pause