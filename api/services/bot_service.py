"""
Servicio para la gestión de bots de trading.
Implementa el patrón de diseño de servicios para separar la lógica de negocio de las rutas.
"""

import os
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path

# Configurar logging
logger = logging.getLogger(__name__)

class BotService:
    """
    Servicio para gestionar los bots de trading.
    Implementa operaciones como obtener, iniciar, detener y consultar el estado de los bots.
    """
    
    def __init__(self):
        """Inicializa el servicio de bots."""
        self.bots_config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'config', 'bots_config.json'
        )
        self.load_bots_config()
    
    def load_bots_config(self):
        """Carga la configuración de los bots desde el archivo de configuración."""
        try:
            if os.path.exists(self.bots_config_path):
                with open(self.bots_config_path, 'r') as f:
                    self.bots_config = json.load(f)
                logger.info(f"Configuración de bots cargada desde {self.bots_config_path}")
            else:
                logger.warning(f"Archivo de configuración no encontrado: {self.bots_config_path}")
                # Configuración por defecto
                self.bots_config = {
                    "sol_bot_15m": {
                        "id": "sol_bot_15m",
                        "name": "SOL Bot 15m",
                        "symbol": "SOLUSDT",
                        "interval": "15m",
                        "path": "~/new-trading-bots/src/spot_bots/sol_bot_15m",
                        "start_script": "start_enhanced.sh",
                        "stop_script": "stop.sh"
                    }
                }
        except Exception as e:
            logger.error(f"Error al cargar la configuración de bots: {str(e)}")
            raise
    
    def get_all_bots(self):
        """
        Obtiene la lista de todos los bots disponibles.
        
        Returns:
            list: Lista de diccionarios con información de los bots.
        """
        try:
            bots_list = []
            for bot_id, bot_config in self.bots_config.items():
                # Obtener el estado actual del bot
                status = self.get_bot_status(bot_id)
                
                # Crear objeto de bot con información básica
                bot_info = {
                    "id": bot_id,
                    "name": bot_config.get("name", bot_id),
                    "symbol": bot_config.get("symbol", ""),
                    "interval": bot_config.get("interval", ""),
                    "status": status,
                    "last_update": datetime.now().isoformat()
                }
                bots_list.append(bot_info)
            
            return bots_list
        except Exception as e:
            logger.error(f"Error al obtener lista de bots: {str(e)}")
            raise
    
    def get_bot(self, bot_id):
        """
        Obtiene información detallada de un bot específico.
        
        Args:
            bot_id (str): ID del bot a consultar.
            
        Returns:
            dict: Diccionario con información detallada del bot.
        """
        try:
            if bot_id not in self.bots_config:
                logger.warning(f"Bot no encontrado: {bot_id}")
                return None
            
            bot_config = self.bots_config[bot_id]
            status = self.get_bot_status(bot_id)
            
            # Obtener información adicional del bot (balance, ganancias, etc.)
            # En una implementación real, esto vendría del estado del bot o de una base de datos
            bot_info = {
                "id": bot_id,
                "name": bot_config.get("name", bot_id),
                "symbol": bot_config.get("symbol", ""),
                "interval": bot_config.get("interval", ""),
                "status": status,
                "last_update": datetime.now().isoformat(),
                "balance": 100.0,  # Valor de ejemplo
                "profit_today": 0.0,  # Valor de ejemplo
                "profit_total": 0.0,  # Valor de ejemplo
                "trades_today": 0,  # Valor de ejemplo
                "trades_total": 0,  # Valor de ejemplo
                "win_rate": 0.0  # Valor de ejemplo
            }
            
            return bot_info
        except Exception as e:
            logger.error(f"Error al obtener información del bot {bot_id}: {str(e)}")
            raise
    
    def start_bot(self, bot_id):
        """
        Inicia un bot específico.
        
        Args:
            bot_id (str): ID del bot a iniciar.
            
        Returns:
            bool: True si el bot se inició correctamente, False en caso contrario.
        """
        try:
            if bot_id not in self.bots_config:
                logger.warning(f"Bot no encontrado: {bot_id}")
                return False
            
            bot_config = self.bots_config[bot_id]
            bot_path = os.path.expanduser(bot_config.get("path", ""))
            start_script = bot_config.get("start_script", "start.sh")
            
            if not os.path.exists(os.path.join(bot_path, start_script)):
                logger.error(f"Script de inicio no encontrado: {os.path.join(bot_path, start_script)}")
                return False
            
            # Ejecutar script de inicio
            command = f"cd {bot_path} && bash {start_script}"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                logger.error(f"Error al iniciar bot {bot_id}: {stderr.decode('utf-8')}")
                return False
            
            logger.info(f"Bot {bot_id} iniciado correctamente")
            return True
        except Exception as e:
            logger.error(f"Error al iniciar bot {bot_id}: {str(e)}")
            raise
    
    def stop_bot(self, bot_id):
        """
        Detiene un bot específico.
        
        Args:
            bot_id (str): ID del bot a detener.
            
        Returns:
            bool: True si el bot se detuvo correctamente, False en caso contrario.
        """
        try:
            if bot_id not in self.bots_config:
                logger.warning(f"Bot no encontrado: {bot_id}")
                return False
            
            bot_config = self.bots_config[bot_id]
            bot_path = os.path.expanduser(bot_config.get("path", ""))
            stop_script = bot_config.get("stop_script", "stop.sh")
            
            if not os.path.exists(os.path.join(bot_path, stop_script)):
                logger.error(f"Script de detención no encontrado: {os.path.join(bot_path, stop_script)}")
                return False
            
            # Ejecutar script de detención
            command = f"cd {bot_path} && bash {stop_script}"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                logger.error(f"Error al detener bot {bot_id}: {stderr.decode('utf-8')}")
                return False
            
            logger.info(f"Bot {bot_id} detenido correctamente")
            return True
        except Exception as e:
            logger.error(f"Error al detener bot {bot_id}: {str(e)}")
            raise
    
    def get_bot_status(self, bot_id):
        """
        Obtiene el estado actual de un bot verificando si el proceso está en ejecución.
        
        Args:
            bot_id (str): ID del bot a consultar.
            
        Returns:
            str: Estado del bot ('active', 'inactive', 'error').
        """
        try:
            if bot_id not in self.bots_config:
                logger.warning(f"Bot no encontrado: {bot_id}")
                return "unknown"
            
            bot_config = self.bots_config[bot_id]
            
            # Verificar si el proceso del bot está en ejecución
            # Buscamos el proceso por nombre (adaptive_main.py para el bot SOL)
            process_name = "adaptive_main.py"
            if bot_id == "sol_bot_15m":
                process_name = "adaptive_main.py"
            # Se pueden agregar más condiciones para otros tipos de bots
            
            # Ejecutar comando ps para verificar si el proceso está en ejecución
            command = f"ps aux | grep '[p]ython3 {process_name}' | wc -l"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            # Convertir la salida a entero
            try:
                process_count = int(stdout.decode('utf-8').strip())
            except ValueError:
                process_count = 0
            
            # Si hay al menos un proceso en ejecución, el bot está activo
            if process_count > 0:
                logger.info(f"Bot {bot_id} está activo con {process_count} procesos en ejecución")
                return "active"
            else:
                logger.info(f"Bot {bot_id} no está en ejecución")
                return "inactive"
        except Exception as e:
            logger.error(f"Error al obtener estado del bot {bot_id}: {str(e)}")
            return "error"
