# Trading Bots API

API para monitorear y controlar los bots de trading.

## Estructura del Proyecto

```
trading-bots-api/
├── app/
│   ├── config/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   └── utils/
├── app.py
├── update_api_config.sh
```

## Configuración

1. Crea un archivo `.env` basado en `.env.example`
2. Ejecuta la API con:
   ```
   python app.py
   ```

## Scripts de Utilidad

- `update_api_config.sh`: Actualiza la configuración de la API para incluir nuevos bots
