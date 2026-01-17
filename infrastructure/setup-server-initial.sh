#!/bin/bash

# Initial Server Bootstrap (one-time, interactive)
# - Creates a 'dev' user (interactive password)
# - Installs fish shell and sets it as default for 'dev'
# - Installs Docker and Docker Compose
# - Configures UFW firewall for SSH/HTTP/HTTPS
# - Sets up nginx reverse proxy for multi-app deployment

set -euo pipefail

echo '🚀 Initial server bootstrap starting...'

# Ensure base packages
sudo apt-get update
sudo apt-get install -y git curl ca-certificates ufw fish sudo make postgresql-client cron nginx certbot python3-certbot-nginx

# Create 'dev' user if missing (interactive password)
if ! id -u dev >/dev/null 2>&1; then
  echo '👤 Creating user "dev" (you will be prompted for password and details)'
  sudo adduser dev
  sudo usermod -aG sudo dev
fi

# Install Docker if not present
if ! command -v docker >/dev/null 2>&1; then
  echo '📦 Installing Docker...'
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  rm -f get-docker.sh
  sudo usermod -aG docker dev || true
fi

# Install Docker Compose (plugin preferred), with fallback to legacy binary
if ! docker compose version >/dev/null 2>&1 && ! command -v docker-compose >/dev/null 2>&1; then
  echo '📦 Installing Docker Compose plugin...'
  sudo apt-get update
  # Try plugin from apt (Ubuntu 22.04+ provides docker-compose-plugin)
  sudo apt-get install -y docker-compose-plugin || true
fi

# If still missing, install legacy standalone binary
if ! docker compose version >/dev/null 2>&1 && ! command -v docker-compose >/dev/null 2>&1; then
  echo '📦 Installing legacy docker-compose binary (fallback)...'
  sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

# If plugin exists but legacy binary is not present, add a small wrapper for compatibility
if docker compose version >/dev/null 2>&1 && ! command -v docker-compose >/dev/null 2>&1; then
  echo '🔗 Adding docker-compose wrapper to call docker compose'
  echo '#!/bin/sh' | sudo tee /usr/local/bin/docker-compose >/dev/null
  echo 'exec docker compose "$@"' | sudo tee -a /usr/local/bin/docker-compose >/dev/null
  sudo chmod +x /usr/local/bin/docker-compose
fi

# Set default shell for 'dev' to fish
if [ "$(getent passwd dev | cut -d: -f7)" != "/usr/bin/fish" ]; then
  echo '🐟 Setting fish as default shell for user dev'
  sudo chsh -s /usr/bin/fish dev
fi

# Install fishmarks for the dev user
echo '🔖 Installing fishmarks for user dev...'
sudo -u dev fish -c 'curl -L https://github.com/techwizrd/fishmarks/raw/master/install.fish | fish' || true

# Install custom fish functions for systemctl management
echo '🔧 Installing custom fish functions for systemctl management...'
sudo -u dev mkdir -p /home/dev/.config/fish/functions

# Create individual fish function files (fish requires each function in its own file)
sudo tee /home/dev/.config/fish/functions/sstart.fish > /dev/null << 'EOF'
function sstart
    sudo systemctl start $argv
end
EOF

sudo tee /home/dev/.config/fish/functions/sstop.fish > /dev/null << 'EOF'
function sstop
    sudo systemctl stop $argv
end
EOF

sudo tee /home/dev/.config/fish/functions/senable.fish > /dev/null << 'EOF'
function senable
    sudo systemctl enable $argv
end
EOF

sudo tee /home/dev/.config/fish/functions/sdisable.fish > /dev/null << 'EOF'
function sdisable
    sudo systemctl disable $argv
end
EOF

sudo tee /home/dev/.config/fish/functions/sstatus.fish > /dev/null << 'EOF'
function sstatus
    sudo systemctl status $argv
end
EOF

sudo tee /home/dev/.config/fish/functions/srestart.fish > /dev/null << 'EOF'
function srestart
    sudo systemctl restart $argv
end
EOF

sudo tee /home/dev/.config/fish/functions/sdreload.fish > /dev/null << 'EOF'
function sdreload
    sudo systemctl daemon-reload
end
EOF

sudo chown -R dev:dev /home/dev/.config/fish
echo '✅ Fish systemctl functions installed'

# Firewall hardening (idempotent)
echo '🛡️  Configuring UFW...'
sudo ufw default deny incoming || true
sudo ufw default allow outgoing || true
sudo ufw allow OpenSSH || true
sudo ufw allow http || true
sudo ufw allow https || true
if ! sudo ufw status | grep -q 'Status: active'; then
  echo 'y' | sudo ufw enable || true
fi

echo '🔐 SSH hardening...'

# Copy the SSH public key from root's authorized_keys to dev user
KEY_INSTALLED=0

if [ -f /root/.ssh/authorized_keys ]; then
  sudo -u dev mkdir -p /home/dev/.ssh
  sudo cp /root/.ssh/authorized_keys /home/dev/.ssh/authorized_keys
  sudo chown -R dev:dev /home/dev/.ssh
  sudo chmod 700 /home/dev/.ssh
  sudo chmod 600 /home/dev/.ssh/authorized_keys
  KEY_INSTALLED=1
  echo '✅ Copied SSH key from root to user dev.'
else
  echo 'ℹ️  No SSH key found in /root/.ssh/authorized_keys; password login for dev will remain enabled.'
fi

SSHD_CFG='/etc/ssh/sshd_config'
sudo cp "$SSHD_CFG" "${SSHD_CFG}.bak.$(date +%s)" || true

# Ensure key options
if sudo grep -qE '^[#]*\s*PubkeyAuthentication' "$SSHD_CFG"; then
  sudo sed -i 's/^[#]*\s*PubkeyAuthentication.*/PubkeyAuthentication yes/' "$SSHD_CFG" || true
else
  echo 'PubkeyAuthentication yes' | sudo tee -a "$SSHD_CFG" >/dev/null
fi

# Disable root SSH login
if sudo grep -qE '^[#]*\s*PermitRootLogin' "$SSHD_CFG"; then
  sudo sed -i 's/^[#]*\s*PermitRootLogin.*/PermitRootLogin no/' "$SSHD_CFG" || true
else
  echo 'PermitRootLogin no' | sudo tee -a "$SSHD_CFG" >/dev/null
fi

# Disallow empty passwords and other sane defaults
if sudo grep -qE '^[#]*\s*PermitEmptyPasswords' "$SSHD_CFG"; then
  sudo sed -i 's/^[#]*\s*PermitEmptyPasswords.*/PermitEmptyPasswords no/' "$SSHD_CFG" || true
else
  echo 'PermitEmptyPasswords no' | sudo tee -a "$SSHD_CFG" >/dev/null
fi
if sudo grep -qE '^[#]*\s*ChallengeResponseAuthentication' "$SSHD_CFG"; then
  sudo sed -i 's/^[#]*\s*ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' "$SSHD_CFG" || true
else
  echo 'ChallengeResponseAuthentication no' | sudo tee -a "$SSHD_CFG" >/dev/null
fi
if sudo grep -qE '^[#]*\s*X11Forwarding' "$SSHD_CFG"; then
  sudo sed -i 's/^[#]*\s*X11Forwarding.*/X11Forwarding no/' "$SSHD_CFG" || true
else
  echo 'X11Forwarding no' | sudo tee -a "$SSHD_CFG" >/dev/null
fi

# Password authentication policy
if [ "$KEY_INSTALLED" = "1" ]; then
  if sudo grep -qE '^[#]*\s*PasswordAuthentication' "$SSHD_CFG"; then
    sudo sed -i 's/^[#]*\s*PasswordAuthentication.*/PasswordAuthentication no/' "$SSHD_CFG" || true
  else
    echo 'PasswordAuthentication no' | sudo tee -a "$SSHD_CFG" >/dev/null
  fi
  echo '🔒 PasswordAuthentication disabled (key-only auth enabled).'
else
  echo '⚠️  PasswordAuthentication remains enabled because no SSH key was provided.'
fi

# Restart SSH service safely (Ubuntu service name is "ssh")
if systemctl list-units --type=service | grep -q '^ssh\.service'; then
  sudo systemctl restart ssh || true
elif systemctl list-units --type=service | grep -q '^sshd\.service'; then
  sudo systemctl restart sshd || true
else
  sudo service ssh restart || true
fi

# No proxy network needed - using direct port exposure

# Setup nginx for multi-app reverse proxy
echo '🌐 Setting up nginx reverse proxy for multi-app deployment...'
sudo tee /etc/nginx/nginx.conf > /dev/null << 'EOF'
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=general:10m rate=30r/s;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Include app-specific configurations
    include /etc/nginx/sites-enabled/*;
    
    # Default server for unmatched domains
    server {
        listen 80 default_server;
        server_name _;
        
        location / {
            return 200 'Multi-app server is running. Deploy apps using setup-project.sh';
            add_header Content-Type text/plain;
        }
    }
    
}
EOF

# Create nginx sites directories
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled

# Disable the default nginx configuration to avoid conflicts
echo '🔧 Disabling default nginx configuration to prevent conflicts...'
if [ -L "/etc/nginx/sites-enabled/default" ]; then
    echo "Disabling default nginx configuration symlink..."
    sudo rm /etc/nginx/sites-enabled/default
fi

# Also check for default.conf in conf.d (some systems use this)
if [ -f "/etc/nginx/conf.d/default.conf" ]; then
    echo "Disabling default nginx configuration in conf.d..."
    sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.disabled
fi

# Start nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# Configure host nginx to connect to proxy network
echo '🌐 Configuring host nginx to connect to proxy network...'
# Host nginx will connect to containers via their proxy network IPs

echo '✅ Initial server bootstrap complete.'
echo 'Next: log in as user "dev" and run ./server-scripts/setup-project.sh to configure the app.'
