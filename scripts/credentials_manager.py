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

# Rutas de archivos
REPO_ROOT = Path(__file__).parent.parent
TEMPLATE_FILE = REPO_ROOT / "credentials_template.json"
CREDENTIALS_FILE = REPO_ROOT / "credentials.json"
AUTH_CONFIG_FILE = REPO_ROOT / "auth_config.json"

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
    
    jwt_token = credentials.get('api', {}).get('jwt_token')
    if not jwt_token or jwt_token == "TU_TOKEN_JWT_AQUI":
        print("Error: Token JWT no configurado en credentials.json")
        return False
    
    try:
        with open(AUTH_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"jwt_token": jwt_token}, f, indent=4)
        print(f"Token JWT actualizado en {AUTH_CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"Error al actualizar auth_config.json: {e}")
        return False

def get_credential(section, key):
    """Obtiene una credencial específica"""
    credentials = load_credentials()
    if not credentials:
        return None
    
    value = credentials.get(section, {}).get(key)
    if not value or value.startswith("TU_"):
        print(f"Advertencia: La credencial {section}.{key} no está configurada correctamente")
        return None
    
    return value

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso: python credentials_manager.py [comando]")
        print("\nComandos disponibles:")
        print("  init       - Inicializa el archivo de credenciales")
        print("  update     - Actualiza auth_config.json con el token JWT")
        print("  get [sección] [clave] - Obtiene una credencial específica")
        return
    
    command = sys.argv[1]
    
    if command == "init":
        load_credentials()
    elif command == "update":
        update_auth_config()
    elif command == "get" and len(sys.argv) >= 4:
        section = sys.argv[2]
        key = sys.argv[3]
        value = get_credential(section, key)
        if value:
            print(value)
    else:
        print("Comando no reconocido")

if __name__ == "__main__":
    main()
