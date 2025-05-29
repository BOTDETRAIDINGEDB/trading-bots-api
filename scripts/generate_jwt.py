#!/usr/bin/env python3
"""
Generador de Token JWT para Trading Bots API
--------------------------------------------
Este script genera un token JWT válido para autenticación en la API.

IMPORTANTE: Este script debe ejecutarse con python3, NO con python:
    $ python3 scripts/generate_jwt.py

En sistemas Linux/Unix, asegúrate de usar 'python3' explícitamente.
"""

import json
import datetime
import sys
from pathlib import Path

try:
    import jwt
except ImportError:
    print("Error: PyJWT no está instalado. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyjwt"])
    import jwt

# Rutas de archivos
REPO_ROOT = Path(__file__).parent.parent
CREDENTIALS_FILE = REPO_ROOT / "credentials.json"
AUTH_CONFIG_FILE = REPO_ROOT / "auth_config.json"

def load_credentials():
    """Carga las credenciales existentes"""
    try:
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar las credenciales: {e}")
        return None

def generate_jwt():
    """Genera un token JWT válido usando la clave secreta de las credenciales"""
    credentials = load_credentials()
    if not credentials:
        return False
    
    # Obtener el JWT_SECRET del archivo de credenciales
    jwt_secret = credentials.get('env', {}).get('JWT_SECRET')
    if not jwt_secret or jwt_secret.startswith("TU_"):
        print("Error: JWT_SECRET no configurado en credentials.json")
        return False
    
    # Configurar la duración del token
    expiration_hours = credentials.get('api_config', {}).get('jwt_expiration_hours', 24)
    
    # Generar el token JWT
    payload = {
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=expiration_hours),
        'iat': datetime.datetime.now(tz=datetime.timezone.utc),
        'user_id': 'admin',
        'role': 'admin'
    }
    
    try:
        token = jwt.encode(payload, jwt_secret, algorithm='HS256')
        
        # Guardar el token en auth_config.json
        with open(AUTH_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"jwt_token": token}, f, indent=4)
        
        print(f"Token JWT generado y guardado en {AUTH_CONFIG_FILE}")
        print(f"El token expirará en {expiration_hours} horas")
        return True
    except Exception as e:
        print(f"Error al generar el token JWT: {e}")
        return False

if __name__ == "__main__":
    generate_jwt()
