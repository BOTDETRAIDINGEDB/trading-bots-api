# Cliente de API para Trading Bots

Este cliente te permite interactuar con la API de Trading Bots desde la línea de comandos de forma sencilla.

## Configuración

1. Edita el archivo `auth_config.json` en la raíz del proyecto y añade tu token JWT:

```json
{
    "jwt_token": "TU_TOKEN_JWT_AQUI"
}
```

2. Asegúrate de tener instalado Python 3 y el paquete `requests`:

```bash
pip install requests
```

## Uso

```bash
# Verificar el estado de la API
python scripts/api_client.py health

# Listar todos los bots disponibles
python scripts/api_client.py list

# Verificar el estado de un bot específico
python scripts/api_client.py status sol_bot_15m

# Iniciar un bot
python scripts/api_client.py start sol_bot_15m

# Detener un bot
python scripts/api_client.py stop sol_bot_15m
```

## Ejemplos

```bash
# Verificar si la API está funcionando
python scripts/api_client.py health

# Ver el estado del bot de SOL
python scripts/api_client.py status sol_bot_15m
```

## Notas

- Este cliente es solo para uso local y no debe ser compartido públicamente
- El token JWT es sensible y no debe ser compartido
- Puedes modificar el archivo `api_client.py` para añadir más funcionalidades según tus necesidades
