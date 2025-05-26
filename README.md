# Trading Bots API

API REST para gestionar y monitorear bots de trading de criptomonedas.

## Características

- 🔐 **Autenticación JWT**: Protección de rutas con tokens JWT
- 📊 **Gestión de Bots**: Iniciar, detener y monitorear bots de trading
- 🔔 **Webhooks**: Endpoints para recibir notificaciones de Binance, Telegram y TradingView
- 📝 **Logging**: Sistema de registro detallado para monitoreo y depuración
- 🛡️ **Manejo de Errores**: Respuestas de error estandarizadas y registro de excepciones

## Requisitos

- Python 3.8 o superior
- Flask y dependencias (ver `requirements.txt`)
- Acceso a los bots de trading (repositorio `trading-bots`)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/BOTDETRAIDINGEDB/trading-bots-api.git
   cd trading-bots-api
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno:
   - Crea un archivo `.env` basado en `.env.example`
   - Añade tus credenciales y configuraciones

## Estructura del Proyecto

```
trading-bots-api/
├── api/                      # Código fuente principal
│   ├── middleware/           # Middleware (auth, logging)
│   ├── models/               # Modelos de datos
│   ├── routes/               # Rutas de la API
│   ├── utils/                # Utilidades
│   └── app.py                # Aplicación Flask principal
├── config/                   # Archivos de configuración
│   └── api_config.json       # Configuración principal
├── docs/                     # Documentación
├── .env.example              # Plantilla de variables de entorno
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

## Uso

### Iniciar la API

```bash
python api/app.py
```

Por defecto, la API se ejecutará en `http://0.0.0.0:5000`. Puedes configurar el host y puerto en el archivo `.env` o `config/api_config.json`.

### Endpoints Principales

#### Gestión de Bots

- `GET /api/bots`: Lista todos los bots disponibles
- `GET /api/bots/{bot_id}`: Obtiene información detallada de un bot
- `POST /api/bots/{bot_id}/start`: Inicia un bot
- `POST /api/bots/{bot_id}/stop`: Detiene un bot

#### Webhooks

- `POST /api/webhooks/binance`: Recibe notificaciones de Binance
- `POST /api/webhooks/telegram`: Recibe comandos de Telegram
- `POST /api/webhooks/trading-view`: Recibe señales de TradingView

#### Utilidades

- `GET /api/health`: Verifica el estado de la API
- `GET /api/docs`: Documentación de la API

## Autenticación

La API utiliza autenticación JWT. Para acceder a las rutas protegidas, debes incluir un token en el encabezado `Authorization`:

```
Authorization: Bearer <token>
```

Para obtener un token, contacta al administrador del sistema.

## Configuración

### Variables de Entorno

- `API_HOST`: Host para la API (default: 0.0.0.0)
- `API_PORT`: Puerto para la API (default: 5000)
- `API_DEBUG`: Modo debug (default: False)
- `JWT_SECRET_KEY`: Clave secreta para tokens JWT
- `BINANCE_WEBHOOK_SECRET`: Clave para verificar webhooks de Binance
- `TELEGRAM_WEBHOOK_TOKEN`: Token para verificar webhooks de Telegram
- `TRADINGVIEW_WEBHOOK_KEY`: Clave para verificar webhooks de TradingView

### Archivo de Configuración

El archivo `config/api_config.json` contiene configuraciones adicionales como:

- Orígenes permitidos para CORS
- Nivel de logging
- Configuración de bots
- Límites de tasa de solicitudes

## Seguridad

- Todas las rutas (excepto `/api/health` y webhooks) requieren autenticación
- Los webhooks utilizan tokens o firmas HMAC para verificar la autenticidad
- Las contraseñas y claves API nunca se almacenan en texto plano

## Desarrollo

### Ejecutar en Modo Desarrollo

```bash
FLASK_ENV=development python api/app.py
```

### Pruebas

```bash
pytest tests/
```

## Integración con Trading Bots

Esta API está diseñada para trabajar con el repositorio `trading-bots`. Asegúrate de que ambos repositorios estén correctamente configurados y que las rutas en `config/api_config.json` apunten a la ubicación correcta de los scripts de los bots.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estas pautas:
1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo términos privados. Todos los derechos reservados.
