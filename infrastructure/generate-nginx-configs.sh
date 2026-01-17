#!/bin/sh

# Generate nginx configurations for all running apps
# This script scans for running Docker containers and generates nginx configs

set -e

SITES_AVAILABLE="/etc/nginx/sites-available"
SITES_ENABLED="/etc/nginx/sites-enabled"
TEMP_DIR="/tmp/nginx-configs"
mkdir -p "$TEMP_DIR"

# Function to generate nginx config for an app
generate_app_config() {
    local app_name="$1"
    local domain="$2"
    local backend_port="$3"
    local frontend_port="$4"
    
    # Get the assigned port from environment variable or port file
    local nginx_port="${NGINX_PORT}"
    
    # If NGINX_PORT is not set, try to get it from the port assignment file
    if [ -z "$nginx_port" ]; then
        PORT_FILE="/var/lib/multi-app-ports"
        if [ -f "$PORT_FILE" ] && grep -q "^$(basename "$(pwd)"):" "$PORT_FILE" 2>/dev/null; then
            nginx_port=$(grep "^$(basename "$(pwd)"):" "$PORT_FILE" | cut -d: -f2)
        else
            nginx_port="8080"  # Fallback default
        fi
    fi
    
    local nginx_target="127.0.0.1:${nginx_port}"
    echo "Generating config for ${app_name} (${domain}) -> nginx container: ${nginx_target}"
    
    # Generate nginx config
    cat > "$TEMP_DIR/${app_name}.conf" << NGINX_EOF
# Auto-generated config for ${app_name}
# HTTP server - redirect to HTTPS
server {
    listen 80;
    server_name ${domain};
    return 301 https://\$host\$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name ${domain};
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/${domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${domain}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Proxy all requests to the app's nginx container
    location / {
        proxy_pass http://${nginx_target};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
NGINX_EOF
}

# Function to clean up old configs for this app
cleanup_old_configs() {
    local app_name="$1"
    echo "Cleaning up old configs for $app_name"
    
    # Remove old symlinks in sites-enabled
    sudo rm -f "$SITES_ENABLED/$app_name"
    
    # Remove old configs in sites-available
    sudo rm -f "$SITES_AVAILABLE/$app_name"
}

# Main execution
echo "Generating nginx configurations for running apps..."

# Clear existing configs
rm -f "$TEMP_DIR"/*

# Get the current directory name as app name
APP_NAME=$(basename "$(pwd)")
echo "App name: $APP_NAME"

# Try to get domain from .env file
DOMAIN=""
if [ -f ".env" ]; then
    DOMAIN=$(grep "^DOMAIN=" .env | cut -d= -f2 | tr -d '\r\n' | head -1 || echo "")
fi

# Default ports (these should match your docker-compose setup)
BACKEND_PORT=9999
FRONTEND_PORT=8081

# Check if containers are running and get actual ports
if docker ps --format "{{.Names}}" | grep -q "_backend_1$"; then
    BACKEND_CONTAINER="${APP_NAME}_backend_1"
    BACKEND_PORT=$(docker port "$BACKEND_CONTAINER" 2>/dev/null | cut -d: -f2 || echo "9999")
fi

if docker ps --format "{{.Names}}" | grep -q "_admin-frontend_1$"; then
    FRONTEND_CONTAINER="${APP_NAME}_admin-frontend_1"
    FRONTEND_PORT=$(docker port "$FRONTEND_CONTAINER" 2>/dev/null | cut -d: -f2 || echo "8081")
fi

echo "Backend port: $BACKEND_PORT"
echo "Frontend port: $FRONTEND_PORT"
echo "Domain: ${DOMAIN:-'not set'}"

# Clean up old configs for this app
cleanup_old_configs "$APP_NAME"

# Also clean up any configs that might have old upstream references
echo "Cleaning up any old nginx configs with upstream references..."
sudo find /etc/nginx/sites-enabled/ -name "*.conf" -exec grep -l "goods-keeper-nginx" {} \; 2>/dev/null | while read file; do
    echo "Removing old config with upstream reference: $file"
    sudo rm -f "$file"
done

# Generate config
generate_app_config "$APP_NAME" "$DOMAIN" "$BACKEND_PORT" "$FRONTEND_PORT"

# Copy generated configs to sites-available and enable them
for config_file in "$TEMP_DIR"/*.conf; do
    if [ -f "$config_file" ]; then
        config_name=$(basename "$config_file")
        echo "Installing nginx config for $config_name"
        
        # Copy to sites-available
        sudo cp "$config_file" "$SITES_AVAILABLE/$config_name"
        
        # Create symlink in sites-enabled
        sudo ln -sf "$SITES_AVAILABLE/$config_name" "$SITES_ENABLED/$config_name"
    fi
done

# Reload nginx configuration
if command -v nginx >/dev/null 2>&1; then
    sudo nginx -t && sudo nginx -s reload
    echo "Nginx configuration reloaded successfully"
else
    echo "Nginx not found, please reload manually"
fi

echo "Nginx configuration generation complete"
