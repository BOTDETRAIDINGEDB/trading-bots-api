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

## Iniciar la API

### Método Oficial (Recomendado)

Utiliza el script oficial para iniciar la API:

```bash
./start_api.sh
```

Este script:
- Verifica que estés en el directorio correcto
- Comprueba si hay una instancia previa ejecutándose
- Inicia la API en una sesión screen (si está disponible)
- Proporciona instrucciones para monitorear los logs

## Autenticación

### Generación de Tokens JWT

Para autenticarte con la API, necesitas generar un token JWT válido. Usa el script incluido:

```bash
python3 scripts/generate_jwt.py
```

**IMPORTANTE:** En sistemas Linux/Unix, asegúrate de usar `python3` explícitamente, no `python`.

El token generado se guarda en el archivo `auth_config.json` y expira en 24 horas.

### Uso del Token JWT

Para usar el token en tus solicitudes a la API:

```bash
# Leer el token generado
TOKEN=$(cat auth_config.json | python3 -c "import sys, json; print(json.load(sys.stdin)['jwt_token'])")

# Usar el token para consultar información
curl -H "Authorization: Bearer $TOKEN" https://tradebotscentral.com/api/bots/sol_bot_15m
```

### Verificación

Para comprobar que la API está funcionando correctamente:

```bash
curl http://localhost:5000/health
```

Deberías recibir un JSON con estado "ok" y la información de tiempo de ejecución.

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

## Bots Disponibles

### SOL Bot 15m (Adaptativo)

Bot de trading para Solana (SOL) con estrategia adaptativa, take profit dinámico y gestión inteligente del capital.

- **Par**: SOLUSDT
- **Intervalo**: 15 minutos
- **Características**:
  - **Take Profit Dinámico**: Se ajusta según volatilidad y tendencia del mercado
  - **Stop Loss Fijo**: 6% del capital para protección contra movimientos bruscos
  - **Gestión Inteligente del Capital**: Adaptación automática a cualquier balance disponible
  - **Modo Aprendizaje**: Comienza con operaciones pequeñas y aumenta gradualmente
  - **Notificaciones Mejoradas**: Informes detallados con iconos atractivos

## Uso

### Iniciar la API

#### Desarrollo Local

```bash
python api/app.py
```

Por defecto, la API se ejecutará en `http://0.0.0.0:5000`. Puedes configurar el host y puerto en el archivo `.env` o `config/api_config.json`.

#### Producción (con systemd)

En producción, la API está configurada como un servicio systemd y accesible a través de HTTPS:

```bash
# Iniciar el servicio
sudo systemctl start trading-bots-api

# Detener el servicio
sudo systemctl stop trading-bots-api

# Reiniciar el servicio
sudo systemctl restart trading-bots-api

# Ver el estado del servicio
sudo systemctl status trading-bots-api

# Ver los logs
sudo journalctl -u trading-bots-api -f
```

La API está disponible en:

```
https://tradebotscentral.com/api/health
```

### Gestión de Tokens JWT

Para generar un nuevo token JWT (necesario para autenticación):

```bash
# Generar un nuevo token JWT
python3 scripts/generate_jwt.py

# El token se guarda automáticamente en auth_config.json
# y expira después de 24 horas por defecto
```

Si el token expira, simplemente ejecuta el comando anterior para generar uno nuevo.

### Acceso desde Aplicaciones Externas

La API puede ser accedida desde cualquier aplicación externa a través de HTTPS:

```javascript
// Ejemplo con JavaScript/Fetch
fetch('https://tradebotscentral.com/api/bots', {
  headers: {
    'Authorization': 'Bearer YOUR_JWT_TOKEN'
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

```python
# Ejemplo con Python/Requests
import requests

headers = {
    'Authorization': 'Bearer YOUR_JWT_TOKEN'
}

response = requests.get('https://tradebotscentral.com/api/bots', headers=headers)
data = response.json()
print(data)
```

Esto permite integrar la API con:
- Aplicaciones web personalizadas
- Plataformas de automatización como Make (Integromat) o Zapier
- Servicios de notificación (Telegram, Discord, etc.)
- Dashboards de monitoreo

### Endpoints Principales

#### Gestión de Bots

- `GET /api/bots`: Lista todos los bots disponibles
- `GET /api/bots/{bot_id}`: Obtiene información detallada de un bot
- `POST /api/bots/{bot_id}/start`: Inicia un bot
- `POST /api/bots/{bot_id}/stop`: Detiene un bot
- `GET /api/bots/{bot_id}/signals`: Obtiene las señales recientes generadas por el bot
- `GET /api/bots/{bot_id}/positions`: Obtiene las posiciones actualmente abiertas por el bot

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
