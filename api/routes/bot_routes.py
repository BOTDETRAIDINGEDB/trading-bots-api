from flask import Blueprint, jsonify, request
import os
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear blueprint
bot_routes = Blueprint('bot_routes', __name__)

@bot_routes.route('/bots', methods=['GET'])
def get_bots():
    """
    Obtiene la lista de bots disponibles.
    
    Returns:
        JSON con la lista de bots y sus estados.
    """
    try:
        # En una implementación real, esto vendría de una base de datos
        bots = [
            {
                "id": "sol_bot_15m",
                "name": "SOL Bot 15m",
                "symbol": "SOLUSDT",
                "interval": "15m",
                "status": "active",
                "last_update": "2025-05-26T08:00:00Z"
            }
        ]
        
        return jsonify({"success": True, "data": bots}), 200
    except Exception as e:
        logger.error(f"Error al obtener bots: {str(e)}")
        return jsonify({"success": False, "error": "Error interno del servidor"}), 500

@bot_routes.route('/bots/<bot_id>', methods=['GET'])
def get_bot(bot_id):
    """
    Obtiene información detallada de un bot específico.
    
    Args:
        bot_id (str): ID del bot a consultar.
        
    Returns:
        JSON con la información del bot.
    """
    try:
        # En una implementación real, esto vendría de una base de datos
        bots = {
            "sol_bot_15m": {
                "id": "sol_bot_15m",
                "name": "SOL Bot 15m",
                "symbol": "SOLUSDT",
                "interval": "15m",
                "status": "active",
                "last_update": "2025-05-26T08:00:00Z",
                "balance": 1000.0,
                "profit_today": 12.5,
                "profit_total": 150.75,
                "trades_today": 3,
                "trades_total": 42,
                "win_rate": 0.68
            }
        }
        
        if bot_id in bots:
            return jsonify({"success": True, "data": bots[bot_id]}), 200
        else:
            return jsonify({"success": False, "error": "Bot no encontrado"}), 404
    except Exception as e:
        logger.error(f"Error al obtener bot {bot_id}: {str(e)}")
        return jsonify({"success": False, "error": "Error interno del servidor"}), 500

@bot_routes.route('/bots/<bot_id>/start', methods=['POST'])
def start_bot(bot_id):
    """
    Inicia un bot específico.
    
    Args:
        bot_id (str): ID del bot a iniciar.
        
    Returns:
        JSON con el resultado de la operación.
    """
    try:
        # Aquí iría la lógica para iniciar el bot
        # Por ejemplo, ejecutar un script o enviar un comando
        
        return jsonify({
            "success": True, 
            "message": f"Bot {bot_id} iniciado correctamente",
            "data": {"status": "active"}
        }), 200
    except Exception as e:
        logger.error(f"Error al iniciar bot {bot_id}: {str(e)}")
        return jsonify({"success": False, "error": "Error al iniciar el bot"}), 500

@bot_routes.route('/bots/<bot_id>/stop', methods=['POST'])
def stop_bot(bot_id):
    """
    Detiene un bot específico.
    
    Args:
        bot_id (str): ID del bot a detener.
        
    Returns:
        JSON con el resultado de la operación.
    """
    try:
        # Aquí iría la lógica para detener el bot
        
        return jsonify({
            "success": True, 
            "message": f"Bot {bot_id} detenido correctamente",
            "data": {"status": "inactive"}
        }), 200
    except Exception as e:
        logger.error(f"Error al detener bot {bot_id}: {str(e)}")
        return jsonify({"success": False, "error": "Error al detener el bot"}), 500

@bot_routes.route('/bots/<bot_id>/signals', methods=['GET'])
def get_bot_signals(bot_id):
    """
    Obtiene las señales recientes generadas por un bot específico.
    
    Args:
        bot_id (str): ID del bot a consultar.
        
    Returns:
        JSON con las señales recientes del bot.
    """
    try:
        # Verificar que el bot existe
        if bot_id != "sol_bot_15m":
            return jsonify({"success": False, "error": "Bot no encontrado"}), 404
            
        # En una implementación real, esto vendría del estado del bot o de una base de datos
        # Aquí simulamos algunas señales para el bot SOL
        signals = [
            {
                "timestamp": "2025-05-26T14:30:00Z",
                "type": "BUY",
                "price": 125.75,
                "strength": 0.85,
                "indicators": {
                    "rsi": 32,
                    "macd": "bullish",
                    "bollinger": "lower_band"
                },
                "ml_prediction": 0.78,
                "executed": True
            },
            {
                "timestamp": "2025-05-26T12:00:00Z",
                "type": "SELL",
                "price": 128.50,
                "strength": 0.72,
                "indicators": {
                    "rsi": 68,
                    "macd": "bearish",
                    "bollinger": "upper_band"
                },
                "ml_prediction": 0.35,
                "executed": True
            },
            {
                "timestamp": "2025-05-26T08:15:00Z",
                "type": "BUY",
                "price": 122.25,
                "strength": 0.91,
                "indicators": {
                    "rsi": 28,
                    "macd": "bullish",
                    "bollinger": "lower_band"
                },
                "ml_prediction": 0.82,
                "executed": True
            }
        ]
        
        return jsonify({"success": True, "data": signals}), 200
    except Exception as e:
        logger.error(f"Error al obtener señales del bot {bot_id}: {str(e)}")
        return jsonify({"success": False, "error": "Error interno del servidor"}), 500

@bot_routes.route('/bots/<bot_id>/positions', methods=['GET'])
def get_bot_positions(bot_id):
    """
    Obtiene las posiciones actualmente abiertas por un bot específico.
    
    Args:
        bot_id (str): ID del bot a consultar.
        
    Returns:
        JSON con las posiciones activas del bot.
    """
    try:
        # Verificar que el bot existe
        if bot_id != "sol_bot_15m":
            return jsonify({"success": False, "error": "Bot no encontrado"}), 404
            
        # En una implementación real, esto vendría del estado del bot o de una base de datos
        # Aquí simulamos una posición activa para el bot SOL
        positions = [
            {
                "id": "pos_12345",
                "symbol": "SOLUSDT",
                "type": "LONG",
                "entry_price": 125.75,
                "current_price": 127.80,
                "quantity": 0.85,
                "value_usdt": 108.63,
                "profit_loss": 1.74,  # Porcentaje
                "profit_loss_usdt": 1.89,
                "entry_time": "2025-05-26T14:30:00Z",
                "duration": "02:25:10",
                "stop_loss": 118.21,  # 6% fijo como especificado
                "take_profit": 132.04,  # Dinámico basado en volatilidad
                "status": "active"
            }
        ]
        
        return jsonify({"success": True, "data": positions}), 200
    except Exception as e:
        logger.error(f"Error al obtener posiciones del bot {bot_id}: {str(e)}")
        return jsonify({"success": False, "error": "Error interno del servidor"}), 500
