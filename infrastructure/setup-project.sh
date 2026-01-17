#!/bin/bash

# Project Setup for Multi-App Deployment
# - Prompts for GitHub org, repo, app name, and domain
# - Sets up SSH keys for GitHub access
# - Clones/updates repo at /var/www/<app-name>
# - Configures environment and deploys with reverse proxy
# 
# Environment variables:
# - NGINX_START_PORT: Override the starting port for nginx container scanning (default: 8080)

set -euo pipefail

echo '🧩 Multi-app project setup starting...'

# Collect basic information
read -rp 'GitHub organization [Zephony]: ' GITHUB_ORG
GITHUB_ORG=${GITHUB_ORG:-Zephony}

read -rp 'GitHub repository name [goods-keeper]: ' GITHUB_REPO
GITHUB_REPO=${GITHUB_REPO:-goods-keeper}

read -rp 'Docker Hub username: ' DOCKERHUB_USERNAME
if [ -z "${DOCKERHUB_USERNAME:-}" ]; then
  echo '❌ Docker Hub username is required for pulling images.'
  exit 1
fi

if [ -z "${GITHUB_ORG:-}" ] || [ -z "${GITHUB_REPO:-}" ]; then
  echo '❌ GitHub org and repo are required.'
  exit 1
fi

read -rp 'Default branch name [demo]: ' DEFAULT_BRANCH
DEFAULT_BRANCH=${DEFAULT_BRANCH:-demo}

read -rp 'Docker image tag [will use git commit SHA after repo setup]: ' DOCKER_TAG

DEFAULT_APP_NAME="$GITHUB_REPO"
read -rp "App name [default: $DEFAULT_APP_NAME]: " APP_NAME
APP_NAME=${APP_NAME:-$DEFAULT_APP_NAME}

read -rp 'Domain [goods-keeper.getpreview.io]: ' DOMAIN_BASE
DOMAIN_BASE=${DOMAIN_BASE:-goods-keeper.getpreview.io}
INCLUDE_WWW="N"
if [ -n "${DOMAIN_BASE:-}" ]; then
  read -rp 'Include www subdomain? [y/N]: ' INCLUDE_WWW
  INCLUDE_WWW=${INCLUDE_WWW:-N}
fi

# Ask about backup configuration
read -rp 'Enable database backup? [y/N]: ' ENABLE_BACKUP
ENABLE_BACKUP=${ENABLE_BACKUP:-N}

# Setup paths
APP_DIR_PARENT="/var/www"
APP_DIR="$APP_DIR_PARENT/$APP_NAME"

echo "📁 Setting up app: $APP_NAME at $APP_DIR"

# Configure SSH for GitHub access
echo '🔑 Setting up SSH for GitHub access...'
SSH_DIR="$HOME/.ssh"
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

# Generate SSH key
KEY_ID="id_ed25519_${GITHUB_ORG}_${GITHUB_REPO}"
KEY_ID="$(echo "$KEY_ID" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9_' '_')"
KEY_PATH="$SSH_DIR/$KEY_ID"

if [ ! -f "$KEY_PATH" ]; then
  echo "🔑 Generating SSH key: $KEY_PATH"
  ssh-keygen -t ed25519 -C "deploy-$GITHUB_ORG/$GITHUB_REPO@$(hostname)" -f "$KEY_PATH" -N ''
fi
chmod 600 "$KEY_PATH"
chmod 644 "$KEY_PATH.pub"

# Configure SSH
ssh-keyscan -H github.com 2>/dev/null >> "$SSH_DIR/known_hosts" || true
chmod 644 "$SSH_DIR/known_hosts"

SSH_CONFIG="$SSH_DIR/config"
# Create unique host alias for this app
GITHUB_HOST_ALIAS="github-${GITHUB_ORG}-${GITHUB_REPO}"
GITHUB_HOST_ALIAS="$(echo "$GITHUB_HOST_ALIAS" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9-' '-')"

if ! grep -q "Host $GITHUB_HOST_ALIAS" "$SSH_CONFIG" 2>/dev/null; then
  cat >> "$SSH_CONFIG" << EOF
Host $GITHUB_HOST_ALIAS
  HostName github.com
  User git
  IdentityFile $KEY_PATH
  IdentitiesOnly yes
EOF
  chmod 600 "$SSH_CONFIG"
fi

# Set up repository URL using the unique host alias
REPO_URL="git@$GITHUB_HOST_ALIAS:$GITHUB_ORG/$GITHUB_REPO.git"

echo ""
echo "🚪 Add this SSH public key to GitHub:"
echo "   Settings → SSH and GPG keys → New SSH key"
echo ""
echo "----- BEGIN PUBLIC KEY -----"
cat "$KEY_PATH.pub"
echo "----- END PUBLIC KEY -----"
echo ""

read -rp 'Press Enter after adding the SSH key to GitHub...'

# Setup app directory
sudo mkdir -p "$APP_DIR_PARENT"
sudo chown -R "$USER":"$USER" "$APP_DIR_PARENT"

# Clone or update repository
if [ -d "$APP_DIR/.git" ]; then
  echo '🔄 Updating existing repository...'
  git -C "$APP_DIR" remote set-url origin "$REPO_URL" || true
  git -C "$APP_DIR" fetch --all --prune
  git -C "$APP_DIR" checkout "$DEFAULT_BRANCH" 2>/dev/null || git -C "$APP_DIR" checkout -b "$DEFAULT_BRANCH"
  git -C "$APP_DIR" reset --hard "origin/$DEFAULT_BRANCH"
else
  echo "🔗 Cloning $REPO_URL into $APP_DIR"
  git clone --branch "$DEFAULT_BRANCH" --single-branch "$REPO_URL" "$APP_DIR" || {
    echo "Clone with specified branch failed; falling back to default branch..."
    git clone "$REPO_URL" "$APP_DIR"
  }
fi

cd "$APP_DIR"

# Get the current git commit SHA after repo is available
GIT_COMMIT_SHA=$(git rev-parse HEAD 2>/dev/null || echo "")
if [ -z "$GIT_COMMIT_SHA" ]; then
  echo '❌ Could not determine git commit SHA from repository.'
  exit 1
fi

# Use git commit SHA as default if no tag was specified
if [ -z "$DOCKER_TAG" ]; then
  DOCKER_TAG="$GIT_COMMIT_SHA"
  echo "🔖 Using git commit SHA as image tag: $DOCKER_TAG"
else
  echo "🔖 Using specified image tag: $DOCKER_TAG"
fi

# Check Docker Compose
if docker compose version >/dev/null 2>&1; then
  COMPOSE='docker compose'
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE='docker-compose'
else
  echo '❌ Docker Compose is required. Please run server-scripts/setup-server-initial.sh first.'
  exit 1
fi

# Copy nginx config generator script
echo '📝 Setting up nginx config generator...'
mkdir -p scripts

# Find the generate-nginx-configs.sh script
if [ -f "$(dirname "$0")/generate-nginx-configs.sh" ]; then
  cp "$(dirname "$0")/generate-nginx-configs.sh" scripts/
elif [ -f "./infrastructure/generate-nginx-configs.sh" ]; then
  cp "./infrastructure/generate-nginx-configs.sh" scripts/
else
  echo "❌ Could not find generate-nginx-configs.sh script"
  exit 1
fi

chmod +x scripts/generate-nginx-configs.sh

# Setup environment
echo '🔧 Configuring environment...'
if [ ! -f .env ]; then
  cp env.example .env
fi

# Generate secure secrets
generate_hex() { openssl rand -hex "$1"; }

if sed --version >/dev/null 2>&1; then SED_I=(sed -i); else SED_I=(sed -i ''); fi

# Update passwords and secrets
DB_PASSWORD=$(grep -E '^POSTGRES_PASSWORD=' .env | cut -d'=' -f2- || true)
if [ -z "${DB_PASSWORD:-}" ] || [[ "$DB_PASSWORD" == 'password' ]]; then
  DB_PASSWORD=$(generate_hex 32)
  "${SED_I[@]}" "s|^POSTGRES_PASSWORD=.*$|POSTGRES_PASSWORD=$DB_PASSWORD|g" .env
fi

RABBITMQ_PASSWORD_VAL=$(grep -E '^RABBITMQ_PASSWORD=' .env | cut -d'=' -f2- || true)
if [ -z "${RABBITMQ_PASSWORD_VAL:-}" ] || [[ "$RABBITMQ_PASSWORD_VAL" == 'guest' ]]; then
  RABBITMQ_PASSWORD_VAL=$(generate_hex 32)
  "${SED_I[@]}" "s|^RABBITMQ_PASSWORD=.*$|RABBITMQ_PASSWORD=$RABBITMQ_PASSWORD_VAL|g" .env
fi

SECRET_KEY_VAL=$(grep -E '^SECRET_KEY=' .env | cut -d'=' -f2- || true)
if [ -z "${SECRET_KEY_VAL:-}" ] || [[ "$SECRET_KEY_VAL" == 'changeme' ]]; then
  SECRET_KEY_VAL=$(generate_hex 64)
  "${SED_I[@]}" "s|^SECRET_KEY=.*$|SECRET_KEY=$SECRET_KEY_VAL|g" .env
fi

# Configure specific database and application variables
echo '🔧 Setting up database and application configuration...'

# POSTGRES_USER
POSTGRES_USER_VAL=$(grep -E '^POSTGRES_USER=' .env | cut -d'=' -f2- || true)
if [ -z "${POSTGRES_USER_VAL:-}" ]; then
  read -rp 'PostgreSQL username [admin]: ' POSTGRES_USER_INPUT
  POSTGRES_USER_VAL=${POSTGRES_USER_INPUT:-admin}
  echo "POSTGRES_USER=$POSTGRES_USER_VAL" >> .env
else
  echo "✅ POSTGRES_USER already set: $POSTGRES_USER_VAL"
fi

# POSTGRES_PASSWORD (use existing logic but ensure it's set)
if [ -z "${DB_PASSWORD:-}" ] || [[ "$DB_PASSWORD" == 'password' ]]; then
  DB_PASSWORD=$(generate_hex 32)
  "${SED_I[@]}" "s|^POSTGRES_PASSWORD=.*$|POSTGRES_PASSWORD=$DB_PASSWORD|g" .env
  echo "✅ Generated new POSTGRES_PASSWORD"
else
  echo "✅ POSTGRES_PASSWORD already set"
fi

# POSTGRES_DB
POSTGRES_DB_VAL=$(grep -E '^POSTGRES_DB=' .env | cut -d'=' -f2- || true)
if [ -z "${POSTGRES_DB_VAL:-}" ]; then
  read -rp 'PostgreSQL database name [goods_keeper]: ' POSTGRES_DB_INPUT
  POSTGRES_DB_VAL=${POSTGRES_DB_INPUT:-goods_keeper}
  echo "POSTGRES_DB=$POSTGRES_DB_VAL" >> .env
else
  echo "✅ POSTGRES_DB already set: $POSTGRES_DB_VAL"
fi

# POSTGRES_PORT
POSTGRES_PORT_VAL=$(grep -E '^POSTGRES_PORT=' .env | cut -d'=' -f2- || true)
if [ -z "${POSTGRES_PORT_VAL:-}" ]; then
  read -rp 'PostgreSQL port [5432]: ' POSTGRES_PORT_INPUT
  POSTGRES_PORT_VAL=${POSTGRES_PORT_INPUT:-5432}
  echo "POSTGRES_PORT=$POSTGRES_PORT_VAL" >> .env
else
  echo "✅ POSTGRES_PORT already set: $POSTGRES_PORT_VAL"
fi

# SECRET_KEY (use existing logic but ensure it's set)
if [ -z "${SECRET_KEY_VAL:-}" ] || [[ "$SECRET_KEY_VAL" == 'changeme' ]]; then
  SECRET_KEY_VAL=$(generate_hex 64)
  "${SED_I[@]}" "s|^SECRET_KEY=.*$|SECRET_KEY=$SECRET_KEY_VAL|g" .env
  echo "✅ Generated new SECRET_KEY"
else
  echo "✅ SECRET_KEY already set"
fi

# Configure domain settings
if [ -n "${DOMAIN_BASE:-}" ]; then
  if [[ "${INCLUDE_WWW^^}" == "Y" ]]; then
    ALLOWED="$DOMAIN_BASE,www.$DOMAIN_BASE"
  else
    ALLOWED="$DOMAIN_BASE"
  fi
  
  # Update environment variables
  grep -q '^ALLOWED_HOSTS=' .env 2>/dev/null || echo "ALLOWED_HOSTS=$ALLOWED" >> .env
  "${SED_I[@]}" "s|^ALLOWED_HOSTS=.*$|ALLOWED_HOSTS=$ALLOWED|g" .env
  
  grep -q '^NEXT_PUBLIC_API_URL=' .env 2>/dev/null || echo "NEXT_PUBLIC_API_URL=https://$DOMAIN_BASE/api" >> .env
  "${SED_I[@]}" "s|^NEXT_PUBLIC_API_URL=.*$|NEXT_PUBLIC_API_URL=https://$DOMAIN_BASE/api|g" .env
  
  grep -q '^DOMAIN=' .env 2>/dev/null || echo "DOMAIN=$DOMAIN_BASE" >> .env
  "${SED_I[@]}" "s|^DOMAIN=.*$|DOMAIN=$DOMAIN_BASE|g" .env
fi

chmod 600 .env

# Setup directories
mkdir -p uploads files
chown $(id -u):$(id -g) uploads files || true
chmod 775 uploads || true

# Setup SSL certificates for host nginx (if domain provided)
if [ -n "${DOMAIN_BASE:-}" ]; then
  echo "🔐 Setting up SSL certificates for host nginx..."
  
  # Try to get Let's Encrypt certificate
  if command -v certbot >/dev/null 2>&1; then
    sudo systemctl stop nginx 2>/dev/null || true
    
    CERT_DOMAINS=("-d" "$DOMAIN_BASE")
    if [[ "${INCLUDE_WWW^^}" == "Y" ]]; then
      CERT_DOMAINS+=("-d" "www.$DOMAIN_BASE")
    fi
    
    if sudo certbot certonly --standalone "${CERT_DOMAINS[@]}" --non-interactive --agree-tos -m "admin@$DOMAIN_BASE" 2>/dev/null; then
      echo "✅ SSL certificates installed for host nginx"
    else
      echo "⚠️  Let's Encrypt failed, no SSL certificate installed"
    fi
    
    sudo systemctl start nginx
  else
    echo "⚠️  Certbot not available, no SSL certificate installed"
  fi
fi

# Setup backup if enabled
if [[ "$ENABLE_BACKUP" =~ ^[Yy]$ ]]; then
  chmod +x scripts/db_backup.sh 2>/dev/null || true
  
  read -rp 'Install daily backup cron job? [Y/n]: ' INSTALL_BACKUP_CRON
  INSTALL_BACKUP_CRON=${INSTALL_BACKUP_CRON:-Y}
  if [[ "$INSTALL_BACKUP_CRON" =~ ^[Yy]$ ]]; then
    sudo mkdir -p /var/backups/$APP_NAME/db
    sudo chown $(id -u):$(id -g) /var/backups/$APP_NAME/db || true
    CRON_LINE="5 3 * * * BACKUP_DIR=/var/backups/$APP_NAME/db /bin/bash $APP_DIR/scripts/db_backup.sh >> /var/backups/$APP_NAME/db/backup.log 2>&1"
    (crontab -l 2>/dev/null | grep -v -F "$CRON_LINE" ; echo "$CRON_LINE") | crontab -
    echo '🗓️  Backup cron job installed'
  fi
fi

# Assign port for nginx container
echo '🔌 Assigning port for nginx container...'
PORT_FILE="/var/lib/multi-app-ports"
# Starting port for scanning (can be overridden with NGINX_START_PORT)
NGINX_START_PORT=${NGINX_START_PORT:-8080}

# Create port file if it doesn't exist
if [ ! -f "$PORT_FILE" ]; then
  sudo mkdir -p "$(dirname "$PORT_FILE")"
  sudo touch "$PORT_FILE"
  sudo chmod 666 "$PORT_FILE"
fi

# Check if this app already has a port assigned
if grep -q "^${APP_NAME}:" "$PORT_FILE" 2>/dev/null; then
  NGINX_PORT=$(grep "^${APP_NAME}:" "$PORT_FILE" | cut -d: -f2)
  echo "✅ Using existing port $NGINX_PORT for $APP_NAME"
else
  # Find next available port starting from the configured start port
  NGINX_PORT=$NGINX_START_PORT
  while [ $NGINX_PORT -lt 9000 ]; do
    # Check if port is already assigned to another app
    if ! grep -q ":$NGINX_PORT$" "$PORT_FILE" 2>/dev/null; then
      # Check if port is actually free on the system
      if ! netstat -tuln 2>/dev/null | grep -q ":$NGINX_PORT "; then
        # Assign port to this app
        echo "${APP_NAME}:${NGINX_PORT}" >> "$PORT_FILE"
        echo "✅ Assigned new port $NGINX_PORT for $APP_NAME"
        break
      fi
    fi
    NGINX_PORT=$((NGINX_PORT + 1))
  done
  
  if [ $NGINX_PORT -ge 9000 ]; then
    echo "❌ No available ports found (checked ${NGINX_START_PORT}-8999)"
    exit 1
  fi
fi

# Export the port for docker-compose to use
export NGINX_PORT

# Update NGINX_PORT in .env file for this deployment
grep -q '^NGINX_PORT=' .env 2>/dev/null || echo "NGINX_PORT=$NGINX_PORT" >> .env
"${SED_I[@]}" "s|^NGINX_PORT=.*$|NGINX_PORT=$NGINX_PORT|g" .env

# Deploy the application
echo '🚀 Deploying application...'

# Set project name to avoid conflicts
export COMPOSE_PROJECT_NAME="$APP_NAME"

# Use a temporary Docker config to avoid persisting credentials on disk
export DOCKER_CONFIG=$(mktemp -d)

# Log in to Docker Hub to pull images
echo '🔐 Logging in to Docker Hub...'
read -sp 'Docker Hub token: ' DOCKERHUB_TOKEN
echo ""
echo "$DOCKERHUB_TOKEN" | docker login docker.io -u "$DOCKERHUB_USERNAME" --password-stdin

# Try to pull images from Docker Hub first, fall back to building if they don't exist
echo '📝 Attempting to pull images from Docker Hub...'

# Extract services with build configurations from production compose files
echo '🔍 Detecting services with build configurations...'
SERVICES_WITH_BUILD=$(docker-compose -f docker-compose.yml -f docker-compose.production.yml config --services | while read service; do
  if docker-compose -f docker-compose.yml -f docker-compose.production.yml config | grep -A 20 "^  $service:" | grep -q "build:"; then
    echo "$service"
  fi
done)

if [ -z "$SERVICES_WITH_BUILD" ]; then
  echo '❌ No services with build configurations found. This script requires services with build configs to pull from Docker Hub.'
  exit 1
else
  echo "📦 Found services with build configs: $(echo $SERVICES_WITH_BUILD | tr '\n' ' ')"
  
  # Check if all images exist on Docker Hub
  MISSING_IMAGES=()
  for service in $SERVICES_WITH_BUILD; do
    IMAGE_NAME="docker.io/${DOCKERHUB_USERNAME}/tds-admin-${service}:${DOCKER_TAG}"
    echo "🔍 Checking for image: $IMAGE_NAME"
    if ! docker pull "$IMAGE_NAME" >/dev/null 2>&1; then
      echo "❌ Image not found: $IMAGE_NAME"
      MISSING_IMAGES+=("$IMAGE_NAME")
    else
      echo "✅ Image found: $IMAGE_NAME"
    fi
  done
  
  if [ ${#MISSING_IMAGES[@]} -gt 0 ]; then
    echo ""
    echo "❌ The following images were not found on Docker Hub:"
    for image in "${MISSING_IMAGES[@]}"; do
      echo "   - $image"
    done
    echo ""
    echo "Please ensure:"
    echo "1. Images are built and pushed to Docker Hub with the correct names"
    echo "2. The Docker Hub username is correct: $DOCKERHUB_USERNAME"
    echo "3. The image tag is correct: $DOCKER_TAG (current commit: $GIT_COMMIT_SHA)"
    echo "4. You have access to the Docker Hub repository"
    echo "5. The CI/CD pipeline has built and pushed images for this commit"
    echo ""
    echo "Expected image naming convention: docker.io/{username}/tds-admin-{service}:{commit-sha}"
    exit 1
  fi
  
  echo '✅ All images found on Docker Hub, using pre-built images...'
  # Create override file to use Docker Hub images
  printf "%s\n" "services:" > docker-compose.deploy.yml
  for service in $SERVICES_WITH_BUILD; do
    IMAGE_NAME="docker.io/${DOCKERHUB_USERNAME}/tds-admin-${service}:${DOCKER_TAG}"
    printf "  %s:\n    image: %s\n" "$service" "$IMAGE_NAME" >> docker-compose.deploy.yml
  done
  
  # Deploy using Docker Hub images
  $COMPOSE -f docker-compose.yml -f docker-compose.production.yml -f docker-compose.deploy.yml up -d --no-build
fi

# Wait for services to be healthy
echo '⏳ Waiting for services to be healthy...'
sleep 15

# Seed the database
echo '🌱 Seeding database...'
if [ -f docker-compose.deploy.yml ]; then
  # Using Docker Hub images
  $COMPOSE -f docker-compose.yml -f docker-compose.production.yml -f docker-compose.deploy.yml exec -T backend sh -lc 'python -m backend.scripts rebuild' || {
    echo '⚠️  Database seeding failed, but continuing with deployment...'
  }
else
  # Using local build
  $COMPOSE -f docker-compose.yml -f docker-compose.production.yml exec -T backend sh -lc 'python -m backend.scripts rebuild' || {
    echo '⚠️  Database seeding failed, but continuing with deployment...'
  }
fi

# Generate nginx configuration
echo '🔧 Generating nginx configuration...'
chmod +x scripts/generate-nginx-configs.sh
sudo ./scripts/generate-nginx-configs.sh

# Clean up Docker credentials and temporary files
echo '🧹 Cleaning up Docker credentials...'
docker logout docker.io || true
rm -rf "$DOCKER_CONFIG" || true
rm -f docker-compose.deploy.yml || true

# Add cleanup function for port management
echo '🧹 Setting up port cleanup...'
cat > "scripts/cleanup-ports.sh" << 'EOF'
#!/bin/bash
# Cleanup script to remove port assignment when app is stopped
APP_NAME=$(basename "$(pwd)")
PORT_FILE="/var/lib/multi-app-ports"

if [ -f "$PORT_FILE" ] && grep -q "^${APP_NAME}:" "$PORT_FILE" 2>/dev/null; then
  # Remove the app's port assignment
  grep -v "^${APP_NAME}:" "$PORT_FILE" > "${PORT_FILE}.tmp" 2>/dev/null || true
  mv "${PORT_FILE}.tmp" "$PORT_FILE" 2>/dev/null || true
  echo "✅ Released port assignment for $APP_NAME"
fi
EOF
chmod +x scripts/cleanup-ports.sh

echo '✅ Project setup complete!'
echo ""
echo "📋 Summary:"
echo "- App: $APP_NAME"
echo "- Directory: $APP_DIR"
echo "- Mode: Multi-app (reverse proxy)"
if [ -n "${DOMAIN_BASE:-}" ]; then
  if [[ "${INCLUDE_WWW^^}" == "Y" ]]; then
    echo "- URLs: https://$DOMAIN_BASE and https://www.$DOMAIN_BASE"
  else
    echo "- URL: https://$DOMAIN_BASE"
  fi
else
  echo "- URL: http://localhost (local development)"
fi
if [[ "$ENABLE_BACKUP" =~ ^[Yy]$ ]]; then
  echo "- Backup: Enabled"
fi

echo ""
echo "🔧 Management commands:"
echo "- View logs: $COMPOSE -f docker-compose.yml -f docker-compose.production.yml logs -f"
echo "- Restart: $COMPOSE -f docker-compose.yml -f docker-compose.production.yml restart"
echo "- Stop: ./scripts/stop-app.sh"
echo "- Update: git pull && $COMPOSE -f docker-compose.yml -f docker-compose.production.yml up -d --pull always"
