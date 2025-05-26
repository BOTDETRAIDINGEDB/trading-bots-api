from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api.log')
    ]
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde .env
load_dotenv()

# Añadir el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar rutas y middleware
from api.routes.bot_routes import bot_routes
from api.routes.webhook_routes import webhook_routes
from api.middleware.auth import auth_middleware
from api.middleware.logging import logging_middleware, log_response
from api.utils.error_handler import register_error_handlers, APIError

# Cargar configuración
try:
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            'config', 'api_config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    logger.info(f"Configuración cargada desde {config_path}")
except Exception as e:
    logger.error(f"Error al cargar la configuración: {str(e)}")
    # Configuración por defecto
    config = {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": False,
        "allowed_origins": ["*"]
    }

# Inicializar Flask
app = Flask(__name__)

# Configurar ProxyFix para manejar correctamente las solicitudes a través de proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configurar CORS
CORS(app, resources={r"/api/*": {"origins": config.get('allowed_origins', ['*'])}})

# Registrar middleware
@app.before_request
def before_request():
    auth_result = auth_middleware()
    if auth_result:
        return auth_result
    logging_middleware()

# Registrar after_request para logging
@app.after_request
def after_request(response):
    return log_response(response)

# Registrar manejadores de errores
register_error_handlers(app)

# Registrar rutas
app.register_blueprint(bot_routes, url_prefix='/api')
app.register_blueprint(webhook_routes, url_prefix='/api')

# Ruta de salud
@app.route('/api/health', methods=['GET'])
def health_check():
    version = "1.0.0"
    start_time = os.getenv('API_START_TIME', datetime.now().isoformat())
    
    return jsonify({
        "success": True,
        "status": "ok",
        "version": version,
        "uptime": f"Desde {start_time}",
        "environment": os.getenv('FLASK_ENV', 'production')
    })

# Ruta para documentación
@app.route('/api/docs', methods=['GET'])
def get_docs():
    try:
        docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')
        return send_from_directory(docs_dir, 'index.html')
    except Exception as e:
        logger.error(f"Error al servir documentación: {str(e)}")
        raise APIError("Documentación no disponible", 404)

# Manejador para rutas no encontradas
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Ruta no encontrada",
        "message": f"La ruta {request.path} no existe en esta API"
    }), 404

if __name__ == '__main__':
    # Registrar tiempo de inicio
    os.environ['API_START_TIME'] = datetime.now().isoformat()
    
    # Detectar si estamos detrás de un proxy
    behind_proxy = os.getenv('BEHIND_PROXY', 'false').lower() == 'true'
    if behind_proxy:
        logger.info("API configurada para ejecutarse detrás de un proxy inverso")
    
    # Usar variables de entorno con valores de config.json como respaldo
    host = os.getenv('API_HOST', config.get('host', '0.0.0.0'))
    port = int(os.getenv('API_PORT', config.get('port', 5000)))
    debug = os.getenv('API_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Iniciando API en {host}:{port} (debug: {debug})")
    app.run(host=host, port=port, debug=debug)
