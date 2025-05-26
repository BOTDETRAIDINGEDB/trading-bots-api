from flask import Blueprint, jsonify, request
import os
import json
import logging
import hmac
import hashlib

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear blueprint
webhook_routes = Blueprint('webhook_routes', __name__)

@webhook_routes.route('/webhooks/binance', methods=['POST'])
def binance_webhook():
    """
    Recibe webhooks de Binance para actualizar el estado de los bots.
    
    Returns:
        JSON con el resultado del procesamiento del webhook.
    """
    try:
        # Verificar la firma del webhook (seguridad)
        signature = request.headers.get('X-Binance-Signature', '')
        secret = os.getenv('BINANCE_WEBHOOK_SECRET', '')
        
        if secret:
            payload = request.get_data().decode('utf-8')
            computed_signature = hmac.new(
                secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, computed_signature):
                logger.warning("Firma de webhook inválida")
                return jsonify({"success": False, "error": "Firma inválida"}), 401
        
        # Procesar el webhook
        data = request.json
        
        # Aquí iría la lógica para procesar el webhook
        # Por ejemplo, actualizar el estado de un bot basado en el evento
        
        logger.info(f"Webhook de Binance procesado: {data.get('event_type', 'desconocido')}")
        
        return jsonify({"success": True, "message": "Webhook procesado correctamente"}), 200
    except Exception as e:
        logger.error(f"Error al procesar webhook de Binance: {str(e)}")
        return jsonify({"success": False, "error": "Error al procesar webhook"}), 500

@webhook_routes.route('/webhooks/telegram', methods=['POST'])
def telegram_webhook():
    """
    Recibe webhooks de Telegram para comandos de bots.
    
    Returns:
        JSON con el resultado del procesamiento del webhook.
    """
    try:
        # Verificar la autenticación del webhook
        token = request.args.get('token', '')
        expected_token = os.getenv('TELEGRAM_WEBHOOK_TOKEN', '')
        
        if not token or token != expected_token:
            logger.warning("Token de webhook de Telegram inválido")
            return jsonify({"success": False, "error": "Token inválido"}), 401
        
        # Procesar el webhook
        data = request.json
        
        # Aquí iría la lógica para procesar comandos de Telegram
        # Por ejemplo, iniciar/detener bots, obtener estadísticas, etc.
        
        logger.info(f"Webhook de Telegram procesado: {data.get('message', {}).get('text', 'desconocido')}")
        
        return jsonify({"success": True, "message": "Webhook procesado correctamente"}), 200
    except Exception as e:
        logger.error(f"Error al procesar webhook de Telegram: {str(e)}")
        return jsonify({"success": False, "error": "Error al procesar webhook"}), 500

@webhook_routes.route('/webhooks/trading-view', methods=['POST'])
def trading_view_webhook():
    """
    Recibe webhooks de TradingView para señales de trading.
    
    Returns:
        JSON con el resultado del procesamiento del webhook.
    """
    try:
        # Verificar la autenticación del webhook
        key = request.args.get('key', '')
        expected_key = os.getenv('TRADINGVIEW_WEBHOOK_KEY', '')
        
        if not key or key != expected_key:
            logger.warning("Clave de webhook de TradingView inválida")
            return jsonify({"success": False, "error": "Clave inválida"}), 401
        
        # Procesar el webhook
        data = request.json
        
        # Aquí iría la lógica para procesar señales de TradingView
        # Por ejemplo, ejecutar órdenes basadas en señales
        
        logger.info(f"Webhook de TradingView procesado: {data.get('strategy', {}).get('action', 'desconocido')}")
        
        return jsonify({"success": True, "message": "Webhook procesado correctamente"}), 200
    except Exception as e:
        logger.error(f"Error al procesar webhook de TradingView: {str(e)}")
        return jsonify({"success": False, "error": "Error al procesar webhook"}), 500
