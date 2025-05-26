#!/bin/bash
# Script para actualizar todas las referencias de 20m a 15m en update_api_config.sh

# Colores para mejor legibilidad
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Actualizando referencias de 20m a 15m en update_api_config.sh ===${NC}"

# Directorio base
BASE_DIR="/home/edisonbautistaruiz2025"
CONFIG_SCRIPT="${BASE_DIR}/update_api_config.sh"

# Verificar que existe el archivo
if [ ! -f "$CONFIG_SCRIPT" ]; then
    echo -e "${RED}Error: El archivo update_api_config.sh no existe: $CONFIG_SCRIPT${NC}"
    exit 1
fi

# Hacer copia de seguridad
BACKUP_FILE="${CONFIG_SCRIPT}.backup.$(date +%Y%m%d%H%M%S)"
cp "$CONFIG_SCRIPT" "$BACKUP_FILE"
echo -e "${GREEN}Copia de seguridad creada: $BACKUP_FILE${NC}"

# Actualizar referencias
echo -e "${YELLOW}Actualizando referencias...${NC}"
sed -i 's|sol_bot_20m|sol_bot_15m|g' "$CONFIG_SCRIPT"
sed -i 's|sol_bot_20min|sol_bot_15min|g' "$CONFIG_SCRIPT"
sed -i 's|"20m"|"15m"|g' "$CONFIG_SCRIPT"

echo -e "${GREEN}Referencias actualizadas correctamente${NC}"
echo -e "${YELLOW}Archivo actualizado: $CONFIG_SCRIPT${NC}"
