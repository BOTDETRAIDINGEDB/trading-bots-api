from flask import request, jsonify
import os
import jwt
import logging
from functools import wraps
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def auth_middleware():
    """
    Middleware de autenticación para proteger rutas de la API.
    
    Verifica que las solicitudes incluyan un token JWT válido en el encabezado
    'Authorization' con el formato 'Bearer <token>'.
    
    Returns:
        None si la autenticación es exitosa, o una respuesta JSON con error si falla.
    """
    # Rutas públicas que no requieren autenticación
    public_routes = [
        '/api/health',
        '/api/docs',
        '/api/webhooks/binance',
        '/api/webhooks/telegram',
        '/api/webhooks/trading-view'
    ]
    
    # Verificar si la ruta es pública
    if request.path in public_routes:
        return None
    
    # Obtener token del encabezado Authorization
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        logger.warning(f"Intento de acceso sin token a {request.path}")
        return jsonify({
            "success": False,
            "error": "No autorizado",
            "message": "Se requiere token de autenticación"
        }), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        # Verificar y decodificar el token
        secret_key = os.getenv('JWT_SECRET_KEY', 'default_secret_key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Verificar expiración (opcional, JWT ya lo hace por defecto)
        if 'exp' in payload and datetime.fromtimestamp(payload['exp']) < datetime.now():
            logger.warning(f"Intento de acceso con token expirado a {request.path}")
            return jsonify({
                "success": False,
                "error": "No autorizado",
                "message": "Token expirado"
            }), 401
        
        # Almacenar información del usuario en el contexto de la solicitud
        # para que esté disponible en los controladores
        request.user = payload
        
        # Autenticación exitosa
        return None
    except jwt.ExpiredSignatureError:
        logger.warning(f"Intento de acceso con token expirado a {request.path}")
        return jsonify({
            "success": False,
            "error": "No autorizado",
            "message": "Token expirado"
        }), 401
    except jwt.InvalidTokenError:
        logger.warning(f"Intento de acceso con token inválido a {request.path}")
        return jsonify({
            "success": False,
            "error": "No autorizado",
            "message": "Token inválido"
        }), 401
    except Exception as e:
        logger.error(f"Error en autenticación: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Error de servidor",
            "message": "Error al procesar la autenticación"
        }), 500

def generate_token(user_id, role='user', expires_in=24):
    """
    Genera un token JWT para un usuario.
    
    Args:
        user_id (str): ID del usuario.
        role (str): Rol del usuario ('user', 'admin', etc.).
        expires_in (int): Tiempo de expiración en horas.
        
    Returns:
        str: Token JWT generado.
    """
    try:
        secret_key = os.getenv('JWT_SECRET_KEY', 'default_secret_key')
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=expires_in),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
    except Exception as e:
        logger.error(f"Error al generar token: {str(e)}")
        raise
