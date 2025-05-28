#!/bin/bash
# Script para configurar la API de Trading Bots con HTTPS y un dominio personalizado
# Uso: ./setup_https_domain.sh [tudominio.com]
# Si no se proporciona un dominio, se usará tradebotscentral.com por defecto

# Colores para mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar si se proporcionó un dominio o usar el predeterminado
if [ $# -eq 0 ]; then
    DOMAIN="tradebotscentral.com"
    echo -e "${YELLOW}No se proporcionó un dominio. Usando el dominio predeterminado: ${GREEN}$DOMAIN${NC}"
else
    DOMAIN=$1
fi
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

# 2. Configurar Nginx como proxy inverso (solo HTTP inicialmente)
echo -e "\n${GREEN}2. Configurando Nginx como proxy inverso...${NC}"
cat > /etc/nginx/sites-available/trading-bots-api <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
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

# Verificar que Nginx esté funcionando antes de continuar
if ! systemctl is-active --quiet nginx; then
    echo -e "${RED}Error: Nginx no está funcionando. Verificando configuración...${NC}"
    nginx -t
    echo -e "${YELLOW}Intentando reiniciar Nginx...${NC}"
    systemctl restart nginx
    sleep 2
    
    if ! systemctl is-active --quiet nginx; then
        echo -e "${RED}Error: No se pudo iniciar Nginx. Revisa la configuración manualmente.${NC}"
        echo -e "${YELLOW}Continuando sin configurar SSL...${NC}"
    fi
fi

# Intentar obtener certificados SSL
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}Obteniendo certificados SSL con Certbot...${NC}"
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || {
        echo -e "${YELLOW}No se pudieron obtener certificados SSL automáticamente.${NC}"
        echo -e "${YELLOW}Posibles razones:${NC}"
        echo -e "  - El dominio aún no apunta a esta IP"
        echo -e "  - Hay problemas con la configuración de Nginx"
        echo -e "${YELLOW}Puedes intentar manualmente más tarde con:${NC}"
        echo -e "  sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
    }
fi

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

# Obtener la IP pública para las instrucciones
PUBLIC_IP=$(curl -s ifconfig.me)

echo -e "\n${GREEN}¡Configuración completada!${NC}"

# Comprobar si Nginx está activo para determinar qué URL mostrar
if systemctl is-active --quiet nginx; then
    echo -e "Tu API está disponible localmente en: ${YELLOW}http://localhost:5000/api/health${NC}"
    echo -e "Tu API está disponible externamente en: ${YELLOW}http://$PUBLIC_IP:80/api/health${NC}"
    
    # Comprobar si los certificados SSL se instalaron correctamente
    if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
        echo -e "Tu API también está disponible con HTTPS en: ${YELLOW}https://$DOMAIN/api/health${NC}"
    else
        echo -e "${YELLOW}Los certificados SSL no se instalaron. Cuando tu dominio apunte a esta IP ($PUBLIC_IP),${NC}"
        echo -e "${YELLOW}podrás obtenerlos manualmente con: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN${NC}"
    fi
else
    echo -e "${RED}Nginx no está funcionando correctamente. Tu API solo está disponible localmente.${NC}"
    echo -e "Puedes acceder localmente en: ${YELLOW}http://localhost:5000/api/health${NC}"
fi

echo -e "Para ver los logs de la API: ${YELLOW}journalctl -u trading-bots-api -f${NC}"

# Instrucciones finales
echo -e "\n${GREEN}Pasos siguientes:${NC}"
echo -e "1. ${YELLOW}Configura tu dominio:${NC} En el panel de Hostinger, crea un registro A para $DOMAIN que apunte a $PUBLIC_IP"
echo -e "2. ${YELLOW}Verifica la conexión:${NC} Espera unos minutos y prueba acceder a http://$DOMAIN/api/health"
echo -e "3. ${YELLOW}Configura SSL:${NC} Si no se configuró automáticamente, ejecuta: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo -e "4. ${YELLOW}Reinicia servicios:${NC} Si cambias la configuración, usa: sudo systemctl restart trading-bots-api nginx"

echo -e "\n${GREEN}Comandos útiles:${NC}"
echo -e "- Ver logs de la API: ${YELLOW}journalctl -u trading-bots-api -f${NC}"
echo -e "- Ver logs de Nginx: ${YELLOW}journalctl -u nginx -f${NC}"
echo -e "- Verificar estado: ${YELLOW}systemctl status trading-bots-api nginx${NC}"
