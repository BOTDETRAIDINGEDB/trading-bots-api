#!/bin/bash

# Script de despliegue para trading-bots-api
LOG_FILE="deploy.log"
echo "=== Iniciando despliegue: $(date) ===" | tee -a $LOG_FILE

# Directorio del proyecto
cd /home/edisonbautistaruiz2025/trading-bots-api

# Crear respaldo antes de actualizar
echo "Creando respaldo..." | tee -a $LOG_FILE
./backup.sh

# Actualizar desde GitHub
echo "Actualizando desde GitHub..." | tee -a $LOG_FILE
git pull

# Actualizar dependencias
echo "Actualizando dependencias..." | tee -a $LOG_FILE
source venv/bin/activate
pip install -r requirements.txt

# Reiniciar la API
echo "Reiniciando la API..." | tee -a $LOG_FILE
./restart_api.sh

echo "=== Despliegue completado: $(date) ===" | tee -a $LOG_FILE
