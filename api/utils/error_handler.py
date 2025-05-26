from flask import jsonify
import logging
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """
    Excepción personalizada para errores de la API.
    
    Atributos:
        message (str): Mensaje de error.
        status_code (int): Código de estado HTTP.
        payload (dict): Datos adicionales para incluir en la respuesta.
    """
    
    def __init__(self, message, status_code=500, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """
        Convierte la excepción a un diccionario para la respuesta JSON.
        
        Returns:
            dict: Representación de la excepción como diccionario.
        """
        response = {
            "success": False,
            "error": self.message
        }
        
        if self.payload:
            response.update(self.payload)
            
        return response

def handle_api_error(error):
    """
    Manejador de errores para excepciones APIError.
    
    Args:
        error (APIError): Excepción a manejar.
        
    Returns:
        tuple: Respuesta JSON y código de estado.
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    
    # Registrar el error
    logger.error(f"API Error: {error.message} (Código: {error.status_code})")
    
    return response

def handle_generic_error(error):
    """
    Manejador de errores para excepciones genéricas.
    
    Args:
        error (Exception): Excepción a manejar.
        
    Returns:
        tuple: Respuesta JSON y código de estado.
    """
    # Registrar el error con stack trace
    logger.error(f"Error no manejado: {str(error)}")
    logger.error(traceback.format_exc())
    
    # Crear respuesta
    response = jsonify({
        "success": False,
        "error": "Error interno del servidor",
        "message": str(error) if not isinstance(error, Exception) else str(error)
    })
    response.status_code = 500
    
    return response

def register_error_handlers(app):
    """
    Registra los manejadores de errores en la aplicación Flask.
    
    Args:
        app: Aplicación Flask.
    """
    # Registrar manejador para APIError
    app.register_error_handler(APIError, handle_api_error)
    
    # Registrar manejadores para errores HTTP comunes
    app.register_error_handler(400, lambda e: handle_api_error(
        APIError("Solicitud incorrecta", 400, {"details": str(e)})
    ))
    app.register_error_handler(401, lambda e: handle_api_error(
        APIError("No autorizado", 401, {"details": str(e)})
    ))
    app.register_error_handler(403, lambda e: handle_api_error(
        APIError("Prohibido", 403, {"details": str(e)})
    ))
    app.register_error_handler(404, lambda e: handle_api_error(
        APIError("Recurso no encontrado", 404, {"details": str(e)})
    ))
    app.register_error_handler(405, lambda e: handle_api_error(
        APIError("Método no permitido", 405, {"details": str(e)})
    ))
    app.register_error_handler(429, lambda e: handle_api_error(
        APIError("Demasiadas solicitudes", 429, {"details": str(e)})
    ))
    
    # Registrar manejador para errores genéricos
    app.register_error_handler(Exception, handle_generic_error)
