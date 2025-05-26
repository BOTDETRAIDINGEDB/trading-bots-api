#!/usr/bin/env python3
"""
Gestor de Credenciales para Trading Bots
----------------------------------------
Este script ayuda a gestionar las credenciales de forma segura.
"""

import json
import os
import sys
from pathlib import Path
import dotenv

# Rutas de archivos
REPO_ROOT = Path(__file__).parent.parent
TEMPLATE_FILE = REPO_ROOT / "credentials_template.json"
CREDENTIALS_FILE = REPO_ROOT / "credentials.json"
AUTH_CONFIG_FILE = REPO_ROOT / "auth_config.json"
ENV_FILE = REPO_ROOT / ".env"

def load_template():
    """Carga la plantilla de credenciales"""
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar la plantilla: {e}")
        return None

def load_credentials():
    """Carga las credenciales existentes o crea un nuevo archivo basado en la plantilla"""
    if not CREDENTIALS_FILE.exists():
        template = load_template()
        if template:
            print(f"Archivo de credenciales no encontrado. Creando uno nuevo basado en la plantilla...")
            with open(CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=4)
            print(f"Archivo de credenciales creado en: {CREDENTIALS_FILE}")
            print(f"Por favor, edita este archivo con tus credenciales reales.")
            return template
        else:
            print("No se pudo crear el archivo de credenciales.")
            return None
    
    try:
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar las credenciales: {e}")
        return None

def update_auth_config():
    """Actualiza el archivo auth_config.json con el token JWT de las credenciales"""
    credentials = load_credentials()
    if not credentials:
        return False
    
    # Obtener el JWT_SECRET del archivo de credenciales
    jwt_secret = credentials.get('env', {}).get('JWT_SECRET')
    if not jwt_secret or jwt_secret.startswith("TU_"):
        print("Error: JWT_SECRET no configurado en credentials.json")
        return False
    
    try:
        with open(AUTH_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"jwt_token": jwt_secret}, f, indent=4)
        print(f"Token JWT actualizado en {AUTH_CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"Error al actualizar auth_config.json: {e}")
        return False

def update_env_file():
    """Actualiza el archivo .env con las variables de entorno del archivo de credenciales"""
    credentials = load_credentials()
    if not credentials:
        return False
    
    env_vars = credentials.get('env', {})
    if not env_vars:
        print("Error: No hay variables de entorno en credentials.json")
        return False
    
    try:
        with open(ENV_FILE, 'w', encoding='utf-8') as f:
            for key, value in env_vars.items():
                if not value.startswith("TU_"):
                    f.write(f"{key}={value}\n")
        print(f"Variables de entorno actualizadas en {ENV_FILE}")
        return True
    except Exception as e:
        print(f"Error al actualizar .env: {e}")
        return False

def update_config_file():
    """Actualiza el archivo de configuración de la API"""
    credentials = load_credentials()
    if not credentials:
        return False
    
    api_config = credentials.get('api_config', {})
    if not api_config:
        print("Error: No hay configuración de API en credentials.json")
        return False
    
    config_dir = REPO_ROOT / "config"
    config_file = config_dir / "api_config.json"
    
    # Crear directorio si no existe
    if not config_dir.exists():
        config_dir.mkdir(parents=True)
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(api_config, f, indent=4)
        print(f"Configuración de API actualizada en {config_file}")
        return True
    except Exception as e:
        print(f"Error al actualizar api_config.json: {e}")
        return False

def get_credential(section, key):
    """Obtiene una credencial específica"""
    credentials = load_credentials()
    if not credentials:
        return None
    
    value = credentials.get(section, {}).get(key)
    if not value or (isinstance(value, str) and value.startswith("TU_")):
        print(f"Advertencia: La credencial {section}.{key} no está configurada correctamente")
        return None
    
    return value

def get_bot_info(bot_id):
    """Obtiene información detallada de un bot específico"""
    credentials = load_credentials()
    if not credentials:
        return None
    
    bots = credentials.get('api_config', {}).get('bots', {})
    bot_info = bots.get(bot_id)
    
    if not bot_info:
        print(f"Advertencia: No se encontró información para el bot {bot_id}")
        return None
    
    return bot_info

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso: python credentials_manager.py [comando]")
        print("\nComandos disponibles:")
        print("  init       - Inicializa el archivo de credenciales")
        print("  update     - Actualiza auth_config.json con el token JWT")
        print("  update-env - Actualiza el archivo .env con las variables de entorno")
        print("  update-config - Actualiza el archivo de configuración de la API")
        print("  update-all - Actualiza todos los archivos de configuración")
        print("  get [sección] [clave] - Obtiene una credencial específica")
        print("  bot [bot_id] - Obtiene información de un bot específico")
        return
    
    command = sys.argv[1]
    
    if command == "init":
        load_credentials()
    elif command == "update":
        update_auth_config()
    elif command == "update-env":
        update_env_file()
    elif command == "update-config":
        update_config_file()
    elif command == "update-all":
        update_auth_config()
        update_env_file()
        update_config_file()
        print("\nTodos los archivos de configuración han sido actualizados.")
    elif command == "get" and len(sys.argv) >= 4:
        section = sys.argv[2]
        key = sys.argv[3]
        value = get_credential(section, key)
        if value:
            print(value)
    elif command == "bot" and len(sys.argv) >= 3:
        bot_id = sys.argv[2]
        bot_info = get_bot_info(bot_id)
        if bot_info:
            print(json.dumps(bot_info, indent=2))
    else:
        print("Comando no reconocido")

if __name__ == "__main__":
    main()
