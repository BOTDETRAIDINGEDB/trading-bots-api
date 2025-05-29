#!/bin/bash
# Script para configurar la renovación automática del token JWT mediante cron
# Autor: Edison Bautista
# Fecha: Mayo 2025

# Colores para mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Configuración de renovación automática de token JWT ===${NC}"

# Obtener la ruta absoluta del directorio del proyecto
PROJECT_DIR=$(cd "$(dirname "$0")/.." && pwd)
RENEW_SCRIPT="$PROJECT_DIR/scripts/renew_token.sh"
LOG_FILE="$PROJECT_DIR/logs/token_renewal.log"

# Crear directorio de logs si no existe
mkdir -p "$PROJECT_DIR/logs"

# Verificar que el script de renovación existe
if [ ! -f "$RENEW_SCRIPT" ]; then
    echo -e "${RED}Error: No se encuentra el script de renovación en $RENEW_SCRIPT${NC}"
    exit 1
fi

# Hacer ejecutable el script de renovación
chmod +x "$RENEW_SCRIPT"
echo -e "${GREEN}Script de renovación configurado como ejecutable${NC}"

# Crear la entrada de cron para ejecutar cada mes (el día 1 a las 00:00)
CRON_ENTRY="0 0 1 * * $RENEW_SCRIPT >> $LOG_FILE 2>&1"

# Verificar si la entrada ya existe en el crontab
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "$RENEW_SCRIPT")

if [ -z "$EXISTING_CRON" ]; then
    # Añadir la nueva entrada al crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo -e "${GREEN}Tarea cron configurada para ejecutarse el día 1 de cada mes a las 00:00${NC}"
else
    echo -e "${YELLOW}La tarea cron ya está configurada${NC}"
fi

# Ejecutar el script de renovación ahora para generar el primer token
echo -e "${GREEN}Ejecutando la primera renovación de token...${NC}"
$RENEW_SCRIPT

echo -e "${GREEN}Configuración completada. El token JWT se renovará automáticamente cada mes.${NC}"
echo -e "${GREEN}Los logs de renovación se guardarán en: $LOG_FILE${NC}"
