#!/bin/bash

# Script oficial para iniciar la API del bot de trading
# Autor: Edison Bautista
# Fecha: Mayo 2025

# Colores para mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Iniciando API del Bot de Trading ===${NC}"

# Verificar que estamos en el directorio correcto
if [ ! -d "api" ] || [ ! -f "api/app.py" ]; then
    echo -e "${RED}Error: No se encuentra el directorio api o el archivo app.py${NC}"
    echo -e "${YELLOW}Asegúrate de ejecutar este script desde el directorio raíz del proyecto trading-bots-api${NC}"
    exit 1
fi

# Verificar entorno virtual
if [ -z "$VIRTUAL_ENV" ] && [ -z "$CONDA_PREFIX" ]; then
    echo -e "${YELLOW}Advertencia: No se detectó un entorno virtual activo.${NC}"
    echo -e "${YELLOW}Se recomienda activar el entorno virtual antes de iniciar la API:${NC}"
    echo -e "${YELLOW}  - Para conda: conda activate ta-lib-env${NC}"
    echo -e "${YELLOW}  - Para venv: source venv/bin/activate${NC}"
    
    read -p "¿Deseas continuar de todos modos? (s/n): " respuesta
    if [[ "$respuesta" != "s" && "$respuesta" != "S" ]]; then
        echo -e "${YELLOW}Operación cancelada por el usuario.${NC}"
        exit 0
    fi
fi

# Verificar si ya hay una instancia de la API ejecutándose
PID=$(ps aux | grep "[p]ython -m api.app" | awk '{print $2}')
if [ ! -z "$PID" ]; then
    echo -e "${YELLOW}¡Advertencia! Ya hay una instancia de la API ejecutándose (PID: $PID)${NC}"
    read -p "¿Deseas detenerla y iniciar una nueva? (s/n): " respuesta
    if [[ "$respuesta" == "s" || "$respuesta" == "S" ]]; then
        echo -e "${YELLOW}Deteniendo instancia anterior...${NC}"
        kill $PID
        sleep 2
    else
        echo -e "${YELLOW}Operación cancelada por el usuario.${NC}"
        exit 0
    fi
fi

# Iniciar la API en segundo plano con screen
if command -v screen &> /dev/null; then
    echo -e "${GREEN}Iniciando API en una sesión screen...${NC}"
    screen -dmS trading-api bash -c "cd $(pwd) && python -m api.app"
    echo -e "${GREEN}API iniciada en segundo plano. Para ver los logs, ejecuta:${NC}"
    echo -e "${YELLOW}  screen -r trading-api${NC}"
    echo -e "${GREEN}Para salir de la sesión screen sin detener la API: Ctrl+A, luego D${NC}"
else
    echo -e "${YELLOW}Screen no está instalado. Iniciando API en primer plano...${NC}"
    echo -e "${YELLOW}Presiona Ctrl+C para detener la API${NC}"
    python -m api.app
fi

echo -e "${GREEN}Para verificar que la API está funcionando, ejecuta:${NC}"
echo -e "${YELLOW}  curl http://localhost:5000/health${NC}"
