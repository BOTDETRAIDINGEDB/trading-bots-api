from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Añadir el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.routes.bot_routes import bot_routes
from api.routes.webhook_routes import webhook_routes
from api.middleware.auth import auth_middleware
from api.middleware.logging import logging_middleware

# Cargar configuración
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                          'config', 'api_config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Inicializar Flask
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": config.get('allowed_origins', ['*'])}})

# Registrar middleware
@app.before_request
def before_request():
    auth_result = auth_middleware()
    if auth_result:
        return auth_result
    logging_middleware()

# Registrar rutas
app.register_blueprint(bot_routes, url_prefix='/api')
app.register_blueprint(webhook_routes, url_prefix='/api')

# Ruta de salud
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "version": "1.0.0"})

# Ruta para documentación
@app.route('/api/docs', methods=['GET'])
def get_docs():
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')
    return send_from_directory(docs_dir, 'index.html')

if __name__ == '__main__':
    # Usar variables de entorno con valores de config.json como respaldo
    host = os.getenv('API_HOST', config.get('host', '0.0.0.0'))
    port = int(os.getenv('API_PORT', config.get('port', 5000)))
    debug = os.getenv('API_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
