from flask import request
import logging
import time
import uuid
import os
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'api.log'))
    ]
)
logger = logging.getLogger(__name__)

def logging_middleware():
    """
    Middleware de logging para registrar información sobre las solicitudes.
    
    Registra detalles como método HTTP, ruta, dirección IP, tiempo de respuesta, etc.
    """
    # Generar un ID único para la solicitud
    request_id = str(uuid.uuid4())
    request.request_id = request_id
    
    # Registrar inicio de la solicitud
    start_time = time.time()
    
    # Almacenar tiempo de inicio para calcular duración
    request.start_time = start_time
    
    # Registrar detalles de la solicitud
    logger.info(f"[{request_id}] Solicitud iniciada: {request.method} {request.path} desde {request.remote_addr}")
    
    # Los datos de la solicitud se registrarán al finalizar en el after_request
    
    # No es necesario devolver nada, ya que este middleware no interrumpe el flujo

def log_response(response):
    """
    Función para registrar información sobre la respuesta.
    
    Args:
        response: Objeto de respuesta Flask.
        
    Returns:
        La misma respuesta sin modificar.
    """
    # Calcular duración de la solicitud
    duration = time.time() - getattr(request, 'start_time', time.time())
    request_id = getattr(request, 'request_id', 'unknown')
    
    # Registrar detalles de la respuesta
    logger.info(
        f"[{request_id}] Solicitud completada: {request.method} {request.path} "
        f"- Estado: {response.status_code} - Duración: {duration:.4f}s"
    )
    
    return response
