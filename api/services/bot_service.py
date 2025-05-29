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
                        "start_script": "start_bot.sh",
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
    
    def get_bot_positions(self, bot_id):
        """
        Obtiene las posiciones actualmente abiertas por un bot específico desde su archivo de estado.
        
        Args:
            bot_id (str): ID del bot a consultar.
            
        Returns:
            list: Lista de diccionarios con información de las posiciones activas.
        """
        try:
            if bot_id not in self.bots_config:
                logger.warning(f"Bot no encontrado: {bot_id}")
                return []
            
            bot_config = self.bots_config[bot_id]
            bot_path = os.path.expanduser(bot_config.get("path", ""))
            
            # Ruta al archivo de estado del bot
            state_file = os.path.join(bot_path, "sol_bot_15min_state.json")
            
            if not os.path.exists(state_file):
                logger.warning(f"Archivo de estado no encontrado: {state_file}")
                return []
            
            # Leer el archivo de estado
            with open(state_file, 'r') as f:
                state = json.load(f)
            
            # Verificar si hay una posición abierta
            if state.get("position", 0) <= 0:
                logger.info(f"Bot {bot_id} no tiene posiciones abiertas")
                return []
            
            # Calcular la duración de la posición
            entry_time = state.get("entry_time", datetime.now().isoformat())
            try:
                entry_datetime = datetime.fromisoformat(entry_time.replace('Z', '+00:00'))
                duration = datetime.now() - entry_datetime
                duration_str = f"{duration.days * 24 + duration.seconds // 3600:02d}:{(duration.seconds % 3600) // 60:02d}:{duration.seconds % 60:02d}"
            except Exception as e:
                logger.error(f"Error al calcular duración de la posición: {str(e)}")
                duration_str = "00:00:00"
            
            # Crear objeto de posición
            position = {
                "id": state.get("position_id", f"pos_{bot_id}_{int(datetime.now().timestamp())}"),
                "symbol": state.get("symbol", ""),
                "type": "LONG" if state.get("position", 0) > 0 else "SHORT",
                "entry_price": state.get("entry_price", 0.0),
                "current_price": state.get("current_price", 0.0),
                "quantity": state.get("position_size", 0.0),
                "value_usdt": state.get("position_amount", 0.0),
                "profit_loss": state.get("current_profit_pct", 0.0),
                "profit_loss_usdt": state.get("current_profit_usdt", 0.0),
                "entry_time": entry_time,
                "duration": duration_str,
                "stop_loss": state.get("stop_loss", 0.0),
                "take_profit": state.get("take_profit", 0.0),
                "status": "active"
            }
            
            return [position]
        except Exception as e:
            logger.error(f"Error al obtener posiciones del bot {bot_id}: {str(e)}")
            return []
            
    def get_bot_signals(self, bot_id):
        """
        Obtiene las señales recientes generadas por un bot específico desde sus logs.
        
        Args:
            bot_id (str): ID del bot a consultar.
            
        Returns:
            list: Lista de diccionarios con información de las señales recientes.
        """
        try:
            if bot_id not in self.bots_config:
                logger.warning(f"Bot no encontrado: {bot_id}")
                return []
            
            bot_config = self.bots_config[bot_id]
            bot_path = os.path.expanduser(bot_config.get("path", ""))
            
            # Ruta al archivo de estado del bot
            state_file = os.path.join(bot_path, "sol_bot_15min_state.json")
            signals_file = os.path.join(bot_path, "signals.json")
            
            # Lista para almacenar las señales
            signals = []
            
            # Verificar si existe el archivo de señales
            if os.path.exists(signals_file):
                try:
                    with open(signals_file, 'r') as f:
                        signals_data = json.load(f)
                        if isinstance(signals_data, list):
                            signals.extend(signals_data)
                except Exception as e:
                    logger.error(f"Error al leer archivo de señales: {str(e)}")
            
            # Si no hay archivo de señales o está vacío, intentar extraer señales del archivo de estado
            if not signals and os.path.exists(state_file):
                try:
                    with open(state_file, 'r') as f:
                        state = json.load(f)
                    
                    # Verificar si hay un historial de operaciones en el estado
                    trades = state.get("trades", [])
                    for trade in trades:
                        # Convertir cada operación en una señal
                        signal = {
                            "timestamp": trade.get("entry_time", ""),
                            "type": "BUY" if trade.get("type", "") == "LONG" else "SELL",
                            "price": trade.get("entry_price", 0.0),
                            "strength": trade.get("signal_strength", 0.5),
                            "indicators": trade.get("indicators", {}),
                            "ml_prediction": trade.get("ml_prediction", 0.5),
                            "executed": True
                        }
                        signals.append(signal)
                except Exception as e:
                    logger.error(f"Error al extraer señales del estado: {str(e)}")
            
            # Si aún no hay señales, buscar en los logs
            if not signals:
                # Buscar archivos de log recientes
                log_dir = os.path.join(bot_path, "logs")
                if os.path.exists(log_dir):
                    try:
                        # Obtener el archivo de log más reciente
                        log_files = [f for f in os.listdir(log_dir) if f.startswith(f"{bot_id}_cloud_simulation_") and f.endswith(".log")]
                        if log_files:
                            log_files.sort(reverse=True)  # Ordenar por nombre (que incluye la fecha)
                            latest_log = os.path.join(log_dir, log_files[0])
                            
                            # Buscar líneas que contengan información de señales
                            with open(latest_log, 'r') as f:
                                log_lines = f.readlines()
                            
                            # Procesar las últimas 1000 líneas del log en busca de señales
                            signal_lines = []
                            for line in log_lines[-1000:]:
                                if "SIGNAL" in line or "signal" in line.lower():
                                    signal_lines.append(line)
                            
                            # Extraer información de las líneas de señales (simplificado)
                            for i, line in enumerate(signal_lines[-10:]):  # Últimas 10 señales
                                try:
                                    # Extraer timestamp
                                    timestamp_str = line.split("[")[1].split("]")[0] if "[" in line and "]" in line else ""
                                    
                                    # Determinar tipo de señal
                                    signal_type = "BUY" if "BUY" in line or "LONG" in line else "SELL" if "SELL" in line or "SHORT" in line else "UNKNOWN"
                                    
                                    # Crear objeto de señal con información básica
                                    signal = {
                                        "timestamp": timestamp_str,
                                        "type": signal_type,
                                        "price": 0.0,  # No podemos extraer esto fácilmente del log
                                        "strength": 0.5,  # Valor por defecto
                                        "indicators": {},
                                        "ml_prediction": 0.5,  # Valor por defecto
                                        "executed": "executed" in line.lower() or "processed" in line.lower()
                                    }
                                    signals.append(signal)
                                except Exception as e:
                                    logger.error(f"Error al procesar línea de señal: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error al procesar logs: {str(e)}")
            
            # Ordenar señales por timestamp (más recientes primero)
            signals.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            # Limitar a las 10 señales más recientes
            return signals[:10]
        except Exception as e:
            logger.error(f"Error al obtener señales del bot {bot_id}: {str(e)}")
            return []
