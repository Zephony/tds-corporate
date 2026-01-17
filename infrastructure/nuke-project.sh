#!/bin/bash

# Project Nuke Script
# Completely removes a project from the server including all containers, volumes, data, and configurations
# Usage: ./nuke-project.sh <project-name>

set -euo pipefail

# Check if project name is provided
if [ $# -eq 0 ]; then
    echo "❌ Error: Project name required"
    echo "Usage: $0 <project-name>"
    echo ""
    echo "This will PERMANENTLY DELETE:"
    echo "   - All containers for the project"
    echo "   - Repository directory /var/www/<project-name>"
    echo "   - Docker volumes for the project"
    echo "   - Database data for the project"
    echo "   - Port assignments for the project"
    echo "   - Nginx configuration for the project"
    echo "   - Backup directory for the project"
    exit 1
fi

PROJECT_NAME="$1"
PROJECT_DIR="/var/www/$PROJECT_NAME"
PORT_FILE="/var/lib/multi-app-ports"

echo "💥 NUKING PROJECT: $PROJECT_NAME"
echo "⚠️  This will PERMANENTLY DELETE:"
echo "   - All containers for $PROJECT_NAME"
echo "   - Repository directory $PROJECT_DIR"
echo "   - Docker volumes for $PROJECT_NAME"
echo "   - Database data for $PROJECT_NAME"
echo "   - Port assignments for $PROJECT_NAME"
echo "   - Nginx configuration for $PROJECT_NAME"
echo "   - Backup directory for $PROJECT_NAME"
echo ""

# Confirmation prompt
read -p "Are you absolutely sure? Type 'NUKE $PROJECT_NAME' to confirm: " confirm
if [ "$confirm" != "NUKE $PROJECT_NAME" ]; then
    echo "❌ Operation cancelled"
    exit 1
fi

echo ""
echo "🔥 Starting complete project destruction..."
echo ""

# Step 1: Stop and remove containers
echo "1️⃣ Stopping and removing containers..."
if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR"
    if [ -f "docker-compose.yml" ]; then
        COMPOSE_PROJECT_NAME="$PROJECT_NAME" docker-compose -f docker-compose.yml -f docker-compose.production.yml down -v --remove-orphans 2>/dev/null || true
    fi
    cd - > /dev/null
fi
echo "✅ Containers stopped and removed"
echo ""

# Step 2: Remove Docker volumes
echo "2️⃣ Removing Docker volumes..."
docker volume ls -q | grep "$PROJECT_NAME" | xargs -r docker volume rm 2>/dev/null || true
echo "✅ Docker volumes removed"
echo ""

# Step 3: Remove port assignment
echo "3️⃣ Removing port assignment..."
if [ -f "$PORT_FILE" ]; then
    sudo sed -i "/^${PROJECT_NAME}:/d" "$PORT_FILE" 2>/dev/null || true
    echo "✅ Port assignment removed"
else
    echo "ℹ️  No port assignment file found"
fi
echo ""

# Step 4: Remove nginx configuration
echo "4️⃣ Removing nginx configuration..."
sudo rm -f "/etc/nginx/sites-available/${PROJECT_NAME}.conf" 2>/dev/null || true
sudo rm -f "/etc/nginx/sites-enabled/${PROJECT_NAME}.conf" 2>/dev/null || true
if sudo nginx -t 2>/dev/null; then
    sudo systemctl reload nginx 2>/dev/null || true
    echo "✅ Nginx configuration removed and reloaded"
else
    echo "⚠️  Nginx configuration removed but reload failed"
fi
echo ""

# Step 5: Remove repository directory
echo "5️⃣ Removing repository directory..."
if [ -d "$PROJECT_DIR" ]; then
    sudo rm -rf "$PROJECT_DIR"
    echo "✅ Repository directory removed"
else
    echo "ℹ️  Repository directory not found"
fi
echo ""

# Step 6: Remove backup directory
echo "6️⃣ Removing backup directory..."
BACKUP_DIR="/var/backups/$PROJECT_NAME"
if [ -d "$BACKUP_DIR" ]; then
    sudo rm -rf "$BACKUP_DIR"
    echo "✅ Backup directory removed"
else
    echo "ℹ️  Backup directory not found"
fi
echo ""

# Step 7: Remove Docker images
echo "7️⃣ Cleaning up Docker images..."
docker images | grep "$PROJECT_NAME" | awk '{print $3}' | xargs -r docker rmi -f 2>/dev/null || true
echo "✅ Docker images removed"
echo ""

# Step 8: Final cleanup
echo "8️⃣ Final cleanup..."
docker system prune -f 2>/dev/null || true
echo "✅ System cleanup completed"
echo ""

# Step 9: Remove any remaining project-specific resources
echo "9️⃣ Removing any remaining project resources..."

# Remove any cron jobs for this project
crontab -l 2>/dev/null | grep -v "$PROJECT_NAME" | crontab - 2>/dev/null || true
echo "✅ Cron jobs removed"

# Remove any systemd services for this project
sudo systemctl stop "${PROJECT_NAME}" 2>/dev/null || true
sudo systemctl disable "${PROJECT_NAME}" 2>/dev/null || true
sudo rm -f "/etc/systemd/system/${PROJECT_NAME}.service" 2>/dev/null || true
sudo systemctl daemon-reload 2>/dev/null || true
echo "✅ Systemd services removed"

echo ""
echo "💥 PROJECT $PROJECT_NAME COMPLETELY NUKED! 💥"
echo "✅ All traces of $PROJECT_NAME have been removed from the server"
echo ""
echo "📋 Summary of what was removed:"
echo "   ✅ Docker containers and services"
echo "   ✅ Docker volumes and database data"
echo "   ✅ Repository directory: $PROJECT_DIR"
echo "   ✅ Backup directory: $BACKUP_DIR"
echo "   ✅ Nginx configuration files"
echo "   ✅ Port assignments"
echo "   ✅ Docker images"
echo "   ✅ Cron jobs"
echo "   ✅ Systemd services"
echo "   ✅ Orphaned Docker resources"
echo ""
echo "🎉 Server is now clean of $PROJECT_NAME!"
