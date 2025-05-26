#!/bin/bash
# Script para actualizar la configuración de la API para incluir el nuevo bot SOL

# Colores para mejor legibilidad
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Actualizando configuración de trading-bots-api ===${NC}"

# Directorio base
BASE_DIR="/home/edisonbautistaruiz2025"
API_DIR="${BASE_DIR}/trading-bots-api"
ENV_FILE="${API_DIR}/.env"
BACKUP_FILE="${API_DIR}/.env.backup.$(date +%Y%m%d%H%M%S)"

# 1. Verificar que existe el directorio de la API
if [ ! -d "$API_DIR" ]; then
    echo -e "${RED}Error: El directorio de la API no existe: $API_DIR${NC}"
    echo -e "${YELLOW}¿Quieres clonar el repositorio? (s/n)${NC}"
    read -r respuesta
    if [[ "$respuesta" =~ ^[Ss]$ ]]; then
        echo -e "${YELLOW}Clonando repositorio de la API...${NC}"
        git clone https://github.com/BOTDETRAIDINGEDB/trading-bots-api.git "$API_DIR"
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error al clonar el repositorio. Abortando.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Operación cancelada.${NC}"
        exit 1
    fi
fi

# 2. Hacer copia de seguridad del archivo .env
if [ -f "$ENV_FILE" ]; then
    cp "$ENV_FILE" "$BACKUP_FILE"
    echo -e "${GREEN}Copia de seguridad creada: $BACKUP_FILE${NC}"
else
    echo -e "${YELLOW}No se encontró archivo .env existente. Se creará uno nuevo.${NC}"
fi

# 3. Actualizar o crear el archivo .env
echo -e "${YELLOW}Actualizando archivo .env...${NC}"

# Si existe el archivo, añadir las nuevas configuraciones
if [ -f "$ENV_FILE" ]; then
    # Verificar si ya existe configuración para SOL_BOT
    if grep -q "SOL_BOT_PATH" "$ENV_FILE"; then
        echo -e "${YELLOW}La configuración para SOL_BOT ya existe. Actualizando...${NC}"
        # Actualizar las rutas existentes
        sed -i '/SOL_BOT_PATH/c\SOL_BOT_PATH='"$BASE_DIR"'/new-trading-bots/src/spot_bots/sol_bot_20m' "$ENV_FILE"
        sed -i '/SOL_BOT_LOG/c\SOL_BOT_LOG='"$BASE_DIR"'/new-trading-bots/src/spot_bots/sol_bot_20m/sol_bot_20min.log' "$ENV_FILE"
        sed -i '/SOL_BOT_STATE/c\SOL_BOT_STATE='"$BASE_DIR"'/new-trading-bots/src/spot_bots/sol_bot_20m/sol_bot_20min_state.json' "$ENV_FILE"
    else
        echo -e "${YELLOW}Añadiendo configuración para SOL_BOT...${NC}"
        # Añadir nuevas configuraciones al final del archivo
        cat >> "$ENV_FILE" << EOF

# Configuración para el bot SOL con reentrenamiento
SOL_BOT_PATH=$BASE_DIR/new-trading-bots/src/spot_bots/sol_bot_20m
SOL_BOT_LOG=$BASE_DIR/new-trading-bots/src/spot_bots/sol_bot_20m/sol_bot_20min.log
SOL_BOT_STATE=$BASE_DIR/new-trading-bots/src/spot_bots/sol_bot_20m/sol_bot_20min_state.json
EOF
    fi
else
    # Crear un nuevo archivo .env basado en .env.example
    echo -e "${YELLOW}Creando nuevo archivo .env...${NC}"
    cat > "$ENV_FILE" << EOF
# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=False

# Security
API_KEY=your_api_key_here
JWT_SECRET=your_jwt_secret_here

# Binance API Keys
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# Bot Paths
XRP_BOT_PATH=$BASE_DIR/new-trading-bots/src/spot_bots/xrp_bot
XRP_BOT_LOG=$BASE_DIR/new-trading-bots/monitor.log
XRP_BOT_STATE=$BASE_DIR/new-trading-bots/src/spot_bots/xrp_bot/bot_state_xrp_30m.json
XRP_BOT_SIMULATION=$BASE_DIR/new-trading-bots/src/spot_bots/xrp_bot/simulation_state_xrp_30m.json

# Configuración para el bot SOL con reentrenamiento
SOL_BOT_PATH=$BASE_DIR/new-trading-bots/src/spot_bots/sol_bot_20m
SOL_BOT_LOG=$BASE_DIR/new-trading-bots/src/spot_bots/sol_bot_20m/sol_bot_20min.log
SOL_BOT_STATE=$BASE_DIR/new-trading-bots/src/spot_bots/sol_bot_20m/sol_bot_20min_state.json

# Notification Settings
TELEGRAM_BOT_TOKEN=your_telegram_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EOF
    echo -e "${YELLOW}IMPORTANTE: Debes editar el archivo .env con tus credenciales reales${NC}"
fi

# 4. Actualizar el código de la API para reconocer el bot SOL
echo -e "${YELLOW}Actualizando el código de la API...${NC}"

# Verificar si existe el archivo de configuración de bots
CONFIG_FILE="${API_DIR}/app/config/bot_config.py"
if [ -f "$CONFIG_FILE" ]; then
    # Hacer copia de seguridad
    cp "$CONFIG_FILE" "${CONFIG_FILE}.backup.$(date +%Y%m%d%H%M%S)"
    
    # Verificar si ya existe configuración para SOL_BOT
    if grep -q "SOL_BOT" "$CONFIG_FILE"; then
        echo -e "${GREEN}La configuración para SOL_BOT ya existe en bot_config.py${NC}"
    else
        echo -e "${YELLOW}Añadiendo configuración para SOL_BOT en bot_config.py...${NC}"
        # Buscar la sección de configuración de bots y añadir SOL_BOT
        sed -i '/BOT_CONFIGS = {/a \    "sol_bot_20m": {\n        "path": os.getenv("SOL_BOT_PATH"),\n        "log_file": os.getenv("SOL_BOT_LOG"),\n        "state_file": os.getenv("SOL_BOT_STATE"),\n        "type": "spot",\n        "symbol": "SOLUSDT",\n        "interval": "20m"\n    },' "$CONFIG_FILE"
    fi
else
    echo -e "${RED}No se encontró el archivo de configuración de bots: $CONFIG_FILE${NC}"
    echo -e "${YELLOW}Es posible que necesites actualizar manualmente la configuración de la API${NC}"
fi

# 5. Reiniciar la API
echo -e "${YELLOW}¿Quieres reiniciar la API ahora? (s/n)${NC}"
read -r respuesta
if [[ "$respuesta" =~ ^[Ss]$ ]]; then
    echo -e "${YELLOW}Reiniciando la API...${NC}"
    
    # Buscar y detener la sesión de screen de la API
    API_SCREEN=$(screen -ls | grep -o "[0-9]*\.trading_api")
    if [ -n "$API_SCREEN" ]; then
        echo -e "${YELLOW}Deteniendo sesión de API existente: $API_SCREEN${NC}"
        screen -S "$API_SCREEN" -X quit
    fi
    
    # Iniciar la API en una nueva sesión de screen
    cd "$API_DIR"
    screen -dmS trading_api python app.py
    echo -e "${GREEN}API reiniciada en sesión screen 'trading_api'${NC}"
else
    echo -e "${YELLOW}No se reinició la API. Puedes hacerlo manualmente cuando lo desees.${NC}"
fi

echo -e "${GREEN}=== Configuración de la API actualizada correctamente ===${NC}"
echo -e "${YELLOW}Para ver los logs de la API:${NC} screen -r trading_api"
echo -e "${YELLOW}Para salir de la vista de logs (sin detener la API):${NC} Presiona Ctrl+A y luego D"
