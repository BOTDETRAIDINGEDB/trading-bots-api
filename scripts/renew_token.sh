#!/bin/bash
# Script para renovar automáticamente el token JWT
# Autor: Edison Bautista
# Fecha: Mayo 2025

# Colores para mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Renovación automática de token JWT ===${NC}"

# Cambiar al directorio del proyecto
cd /home/edisonbautistaruiz2025/trading-bots-api

# Verificar que estamos en el directorio correcto
if [ ! -d "scripts" ] || [ ! -f "scripts/generate_jwt.py" ]; then
    echo -e "${RED}Error: No se encuentra el directorio scripts o el archivo generate_jwt.py${NC}"
    echo -e "${YELLOW}Asegúrate de que la ruta del proyecto es correcta${NC}"
    exit 1
fi

# Generar el nuevo token
echo -e "${GREEN}Generando nuevo token JWT...${NC}"
python3 scripts/generate_jwt.py

# Verificar si se generó correctamente
if [ -f "auth_config.json" ]; then
    TOKEN_DATE=$(date +"%Y-%m-%d %H:%M:%S")
    echo -e "${GREEN}Token JWT renovado exitosamente el ${TOKEN_DATE}${NC}"
    
    # Opcional: Hacer una copia de seguridad del token
    cp auth_config.json auth_config_backup_$(date +"%Y%m%d").json
    
    echo -e "${GREEN}Se ha creado una copia de seguridad del token${NC}"
else
    echo -e "${RED}Error: No se pudo generar el token JWT${NC}"
    exit 1
fi

echo -e "${GREEN}Proceso de renovación completado${NC}"
