#!/usr/bin/env python3
"""
Cliente para la API de Trading Bots
-----------------------------------
Este script permite interactuar con la API de Trading Bots desde la línea de comandos.
"""

import argparse
import json
import os
import sys
import requests
from pathlib import Path

# Configuración
API_BASE_URL = "https://tradebotscentral.com/api"
CONFIG_FILE = Path(__file__).parent.parent / "auth_config.json"

def load_config():
    """Carga la configuración desde el archivo auth_config.json"""
    if not CONFIG_FILE.exists():
        print(f"Error: Archivo de configuración no encontrado en {CONFIG_FILE}")
        print("Crea el archivo con el siguiente formato:")
        print('{\n    "jwt_token": "TU_TOKEN_JWT_AQUI"\n}')
        sys.exit(1)
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al leer el archivo de configuración: {e}")
        sys.exit(1)

def get_headers():
    """Obtiene los headers con el token JWT"""
    config = load_config()
    token = config.get('jwt_token')
    
    if not token or token == "TU_TOKEN_JWT_AQUI":
        print("Error: Token JWT no configurado correctamente")
        print(f"Edita el archivo {CONFIG_FILE} y establece tu token JWT")
        sys.exit(1)
    
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

def check_api_health():
    """Verifica el estado de la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        data = response.json()
        
        if response.status_code == 200 and data.get('success'):
            print("✅ API funcionando correctamente")
            print(f"   Versión: {data.get('version')}")
            print(f"   Uptime: {data.get('uptime')}")
            print(f"   Entorno: {data.get('environment')}")
            return True
        else:
            print("❌ API no está respondiendo correctamente")
            print(f"   Código: {response.status_code}")
            print(f"   Respuesta: {data}")
            return False
    except Exception as e:
        print(f"❌ Error al conectar con la API: {e}")
        return False

def get_bot_status(bot_id):
    """Obtiene el estado de un bot específico"""
    try:
        headers = get_headers()
        response = requests.get(f"{API_BASE_URL}/bots/{bot_id}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                bot_data = data.get('data', {})
                print(f"📊 Estado del bot {bot_id}:")
                print(f"   Estado: {bot_data.get('status', 'Desconocido')}")
                print(f"   Última actualización: {bot_data.get('last_update', 'Desconocido')}")
                
                # Mostrar métricas si están disponibles
                metrics = bot_data.get('metrics', {})
                if metrics:
                    print("\n📈 Métricas:")
                    for key, value in metrics.items():
                        print(f"   {key}: {value}")
                
                # Mostrar configuración
                config = bot_data.get('config', {})
                if config:
                    print("\n⚙️ Configuración:")
                    for key, value in config.items():
                        print(f"   {key}: {value}")
                
                return True
            else:
                print(f"❌ Error: {data.get('error', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Error al obtener estado del bot. Código: {response.status_code}")
            try:
                data = response.json()
                print(f"   Mensaje: {data.get('error', 'No disponible')}")
            except:
                print(f"   Respuesta: {response.text[:100]}...")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def start_bot(bot_id):
    """Inicia un bot específico"""
    try:
        headers = get_headers()
        response = requests.post(f"{API_BASE_URL}/bots/{bot_id}/start", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Bot {bot_id} iniciado correctamente")
                return True
            else:
                print(f"❌ Error: {data.get('error', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Error al iniciar el bot. Código: {response.status_code}")
            try:
                data = response.json()
                print(f"   Mensaje: {data.get('error', 'No disponible')}")
            except:
                print(f"   Respuesta: {response.text[:100]}...")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def stop_bot(bot_id):
    """Detiene un bot específico"""
    try:
        headers = get_headers()
        response = requests.post(f"{API_BASE_URL}/bots/{bot_id}/stop", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Bot {bot_id} detenido correctamente")
                return True
            else:
                print(f"❌ Error: {data.get('error', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Error al detener el bot. Código: {response.status_code}")
            try:
                data = response.json()
                print(f"   Mensaje: {data.get('error', 'No disponible')}")
            except:
                print(f"   Respuesta: {response.text[:100]}...")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def list_bots():
    """Lista todos los bots disponibles"""
    try:
        headers = get_headers()
        response = requests.get(f"{API_BASE_URL}/bots", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                bots = data.get('data', [])
                if not bots:
                    print("ℹ️ No hay bots disponibles")
                    return True
                
                print(f"📋 Bots disponibles ({len(bots)}):")
                for bot in bots:
                    status_emoji = "🟢" if bot.get('status') == "running" else "🔴"
                    print(f"   {status_emoji} {bot.get('id')}: {bot.get('name')} - {bot.get('status')}")
                return True
            else:
                print(f"❌ Error: {data.get('error', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Error al listar bots. Código: {response.status_code}")
            try:
                data = response.json()
                print(f"   Mensaje: {data.get('error', 'No disponible')}")
            except:
                print(f"   Respuesta: {response.text[:100]}...")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Cliente para la API de Trading Bots")
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    # Comando health
    health_parser = subparsers.add_parser("health", help="Verificar el estado de la API")
    
    # Comando list
    list_parser = subparsers.add_parser("list", help="Listar todos los bots disponibles")
    
    # Comando status
    status_parser = subparsers.add_parser("status", help="Obtener el estado de un bot")
    status_parser.add_argument("bot_id", help="ID del bot (ej: sol_bot_15m)")
    
    # Comando start
    start_parser = subparsers.add_parser("start", help="Iniciar un bot")
    start_parser.add_argument("bot_id", help="ID del bot (ej: sol_bot_15m)")
    
    # Comando stop
    stop_parser = subparsers.add_parser("stop", help="Detener un bot")
    stop_parser.add_argument("bot_id", help="ID del bot (ej: sol_bot_15m)")
    
    args = parser.parse_args()
    
    if args.command == "health":
        check_api_health()
    elif args.command == "list":
        list_bots()
    elif args.command == "status":
        get_bot_status(args.bot_id)
    elif args.command == "start":
        start_bot(args.bot_id)
    elif args.command == "stop":
        stop_bot(args.bot_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
