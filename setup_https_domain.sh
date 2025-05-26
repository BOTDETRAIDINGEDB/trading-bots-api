#!/bin/bash
# Script para configurar la API de Trading Bots con HTTPS y un dominio personalizado
# Uso: ./setup_https_domain.sh tudominio.com

# Colores para mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que se proporcionó un dominio
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: Debes proporcionar un dominio.${NC}"
    echo -e "Uso: $0 tudominio.com"
    exit 1
fi

DOMAIN=$1
echo -e "${GREEN}Configurando HTTPS para el dominio: ${YELLOW}$DOMAIN${NC}"

# Verificar que el usuario tiene permisos de sudo
if [ "$(id -u)" != "0" ]; then
   echo -e "${YELLOW}Este script necesita permisos de superusuario.${NC}"
   echo -e "Ejecutando con sudo..."
   sudo "$0" "$@"
   exit $?
fi

# 1. Instalar Nginx si no está instalado
echo -e "\n${GREEN}1. Instalando Nginx...${NC}"
apt update
apt install -y nginx
systemctl enable nginx
systemctl start nginx

# 2. Configurar Nginx como proxy inverso
echo -e "\n${GREEN}2. Configurando Nginx como proxy inverso...${NC}"
cat > /etc/nginx/sites-available/trading-bots-api <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Redirigir todo el tráfico HTTP a HTTPS
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN www.$DOMAIN;
    
    # Los certificados SSL se configurarán automáticamente con Certbot
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Activar la configuración
ln -sf /etc/nginx/sites-available/trading-bots-api /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 3. Instalar Certbot para obtener certificados SSL
echo -e "\n${GREEN}3. Instalando Certbot y obteniendo certificados SSL...${NC}"
apt install -y certbot python3-certbot-nginx
certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# 4. Configurar la API para ejecutarse como servicio
echo -e "\n${GREEN}4. Configurando la API como servicio...${NC}"

# Determinar el usuario actual (el que ejecutó sudo)
ACTUAL_USER=$(logname || echo $SUDO_USER)
API_DIR="/home/$ACTUAL_USER/trading-bots-api"

# Crear el archivo de servicio
cat > /etc/systemd/system/trading-bots-api.service <<EOF
[Unit]
Description=Trading Bots API
After=network.target

[Service]
User=$ACTUAL_USER
WorkingDirectory=$API_DIR
ExecStart=/usr/bin/python3 $API_DIR/api/app.py
Restart=always
Environment="BEHIND_PROXY=true"

[Install]
WantedBy=multi-user.target
EOF

# Recargar systemd, habilitar y iniciar el servicio
systemctl daemon-reload
systemctl enable trading-bots-api
systemctl start trading-bots-api

# 5. Verificar que todo está funcionando
echo -e "\n${GREEN}5. Verificando la configuración...${NC}"
echo -e "Estado de Nginx:"
systemctl status nginx --no-pager
echo -e "\nEstado de la API:"
systemctl status trading-bots-api --no-pager

echo -e "\n${GREEN}¡Configuración completada!${NC}"
echo -e "Tu API ahora está disponible en: ${YELLOW}https://$DOMAIN/api/health${NC}"
echo -e "Para ver los logs de la API: ${YELLOW}journalctl -u trading-bots-api -f${NC}"

# Instrucciones finales
echo -e "\n${GREEN}Notas importantes:${NC}"
echo -e "1. Asegúrate de que tu dominio apunte a la IP de esta máquina virtual"
echo -e "2. Los certificados SSL se renovarán automáticamente"
echo -e "3. Si cambias la configuración de la API, reinicia el servicio con: ${YELLOW}sudo systemctl restart trading-bots-api${NC}"
