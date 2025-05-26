import os
import json
import logging
import subprocess
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Bot:
    """
    Modelo para representar y gestionar un bot de trading.
    """
    
    def __init__(self, bot_id, name, symbol, interval, script_path=None, status="inactive"):
        """
        Inicializa un objeto Bot.
        
        Args:
            bot_id (str): Identificador único del bot.
            name (str): Nombre descriptivo del bot.
            symbol (str): Par de trading (ej. SOLUSDT).
            interval (str): Intervalo de tiempo para las velas (ej. 15m).
            script_path (str, optional): Ruta al script principal del bot.
            status (str, optional): Estado actual del bot ('active' o 'inactive').
        """
        self.id = bot_id
        self.name = name
        self.symbol = symbol
        self.interval = interval
        self.script_path = script_path
        self.status = status
        self.last_update = datetime.now().isoformat()
        self.process = None
        
    def to_dict(self):
        """
        Convierte el objeto Bot a un diccionario.
        
        Returns:
            dict: Representación del bot como diccionario.
        """
        return {
            "id": self.id,
            "name": self.name,
            "symbol": self.symbol,
            "interval": self.interval,
            "status": self.status,
            "last_update": self.last_update
        }
    
    def start(self, simulation=True, balance=1000):
        """
        Inicia el bot.
        
        Args:
            simulation (bool): Si se debe ejecutar en modo simulación.
            balance (float): Balance inicial para simulación.
            
        Returns:
            bool: True si el bot se inició correctamente, False en caso contrario.
        """
        if self.status == "active":
            logger.warning(f"Bot {self.id} ya está activo")
            return False
        
        if not self.script_path or not os.path.exists(self.script_path):
            logger.error(f"Ruta de script no válida para bot {self.id}: {self.script_path}")
            return False
        
        try:
            # Construir comando para iniciar el bot
            cmd = [
                "python", 
                self.script_path, 
                "--symbol", self.symbol,
                "--interval", self.interval,
                "--use-ml",
                "--retrain-interval", "15"
            ]
            
            if simulation:
                cmd.extend(["--simulation", "--balance", str(balance)])
            
            # Iniciar el proceso
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info(f"Bot {self.id} iniciado con PID {self.process.pid}")
            self.status = "active"
            self.last_update = datetime.now().isoformat()
            return True
        except Exception as e:
            logger.error(f"Error al iniciar bot {self.id}: {str(e)}")
            return False
    
    def stop(self):
        """
        Detiene el bot.
        
        Returns:
            bool: True si el bot se detuvo correctamente, False en caso contrario.
        """
        if self.status == "inactive":
            logger.warning(f"Bot {self.id} ya está inactivo")
            return False
        
        try:
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait(timeout=5)
                
                # Si el proceso no terminó, forzar cierre
                if self.process.poll() is None:
                    self.process.kill()
            
            logger.info(f"Bot {self.id} detenido")
            self.status = "inactive"
            self.last_update = datetime.now().isoformat()
            self.process = None
            return True
        except Exception as e:
            logger.error(f"Error al detener bot {self.id}: {str(e)}")
            return False
    
    def get_status(self):
        """
        Obtiene el estado actual del bot.
        
        Returns:
            dict: Estado actual del bot con información adicional.
        """
        status_info = self.to_dict()
        
        # Añadir información adicional (en una implementación real, esto vendría de una base de datos)
        status_info.update({
            "balance": 1000.0,
            "profit_today": 12.5 if self.status == "active" else 0.0,
            "profit_total": 150.75,
            "trades_today": 3 if self.status == "active" else 0,
            "trades_total": 42,
            "win_rate": 0.68
        })
        
        return status_info
    
    @classmethod
    def from_config(cls, bot_id, config):
        """
        Crea un objeto Bot a partir de la configuración.
        
        Args:
            bot_id (str): ID del bot.
            config (dict): Configuración del bot.
            
        Returns:
            Bot: Instancia del bot configurada.
        """
        return cls(
            bot_id=bot_id,
            name=config.get("name", f"Bot {bot_id}"),
            symbol=config.get("symbol", "BTCUSDT"),
            interval=config.get("interval", "1h"),
            script_path=config.get("script_path")
        )
