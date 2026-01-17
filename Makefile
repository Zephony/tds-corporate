# Makefile for TDS Admin Development

# Configuration
IMAGE_NAME = tds-admin
TAG = latest

.PHONY: help dev build prod deploy clean logs status restart reset-data reset-database clean-uploads backend-rebuild db-backup db-restore prod-start prod-stop prod-restart prod-logs prod-status

help: ## Show this help message
	@echo "TDS Admin - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

local: ## Start full stack locally with Docker Compose
	@echo "Starting full stack locally with Docker Compose..."
	docker-compose up -d
	@echo "✅ Full stack started!"
	@echo "🌐 Frontend: http://localhost"
	@echo "🔧 Backend API: http://localhost/api"
	@echo "📚 API Docs: http://localhost/api/docs"
	@echo "🏥 Health Check: http://localhost/health"
	@echo "🌼 Flower Monitoring: http://localhost:5555"
	@echo "⚠️  Note: Frontend disabled for now"

update-postman: ## Update Postman collection from local OpenAPI
	@echo "Updating the Postman collection for TDS Admin..."
	@sh -c 'set -a; [ -f .env ] && . ./.env; set +a; \
	if [ -z "$$POSTMAN_API_KEY" ]; then echo "Error: POSTMAN_API_KEY not set"; exit 1; fi; \
	if [ -z "$$POSTMAN_WORKSPACE_ID" ]; then echo "Error: POSTMAN_WORKSPACE_ID not set"; exit 1; fi; \
	node dev/openapi_to_postmanv2.js --url http://localhost:9999/openapi.json --output postman_collection.json --apikey "$$POSTMAN_API_KEY" --workspace "$$POSTMAN_WORKSPACE_ID"'
	@echo "Postman collection updated successfully!"

build: ## Build production Docker images
	@echo "Building production images..."
	docker build -t tds-admin/backend:latest -f docker/backend/Dockerfile .
	docker build -t tds-admin/celery:latest -f docker/celery/Dockerfile .

prod: ## Start production environment
	@echo "Starting production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

deploy-scripts: ## Copy setup scripts to server /opt/scripts directory (usage: make deploy-scripts TARGET=root@<ipaddr>)
	@echo "Copying setup scripts to server..."
	@if [ -z "$(TARGET)" ]; then echo "Error: TARGET not set. Usage: make deploy-scripts TARGET=root@<ipaddr>"; exit 1; fi
	@echo "Creating /opt/scripts directory on server..."
	ssh $(TARGET) "mkdir -p /opt/scripts"
	@echo "Copying setup scripts..."
	scp infrastructure/setup-server-initial.sh $(TARGET):/opt/scripts/
	scp infrastructure/setup-project.sh $(TARGET):/opt/scripts/
	scp infrastructure/generate-nginx-configs.sh $(TARGET):/opt/scripts/
	scp infrastructure/nuke-project.sh $(TARGET):/opt/scripts/
	@echo "Setting executable permissions..."
	ssh $(TARGET) "chmod +x /opt/scripts/setup-server-initial.sh /opt/scripts/setup-project.sh /opt/scripts/generate-nginx-configs.sh /opt/scripts/nuke-project.sh"
	@echo "Setup scripts copied successfully!"
	@echo "Next steps on server:"
	@echo "  sudo /opt/scripts/setup-server-initial.sh"
	@echo "  sudo /opt/scripts/setup-project.sh"
	@echo "  /opt/scripts/nuke-project.sh <project-name>  # To remove a project"

deploy: ## Deploy to production server
	@echo "Deploying to production..."
	@if [ -z "$(DROPLET_HOST)" ]; then echo "Error: DROPLET_HOST not set"; exit 1; fi
	@if [ -z "$(DROPLET_USER)" ]; then echo "Error: DROPLET_USER not set"; exit 1; fi
	@echo "Note: This is a basic deploy. For multi-app deployment, use infrastructure/setup-project.sh"
	scp docker-compose.yml $(DROPLET_USER)@$(DROPLET_HOST):/var/www/tds-admin/
	scp docker-compose.production.yml $(DROPLET_USER)@$(DROPLET_HOST):/var/www/tds-admin/
	ssh $(DROPLET_USER)@$(DROPLET_HOST) "cd /var/www/tds-admin && COMPOSE_PROJECT_NAME=tds-admin docker compose -f docker-compose.yml -f docker-compose.production.yml up -d"

clean: ## Clean up Docker containers and images
	@echo "Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f

logs: ## Show logs for all services
	docker-compose logs -f

status: ## Show status of all services
	docker-compose ps

restart: ## Restart all services
	@echo "Restarting all services..."
	docker-compose restart

setup-server: ## Set up production server (run on server)
	@echo "Setting up production server..."
	./setup-server.sh

test: ## Run tests
	@echo "Running tests..."
	cd backend && python -m pytest

lint: ## Run linting
	@echo "Running linting..."
	cd backend && flake8 .

format: ## Format code
	@echo "Formatting code..."
	cd backend && black .


# Atomic tasks
clean-uploads: ## Delete all files under uploads/ except .gitkeep
	@echo "Clearing uploads/ (keeping .gitkeep)..."
	find ./uploads -mindepth 1 ! -name '.gitkeep' -exec rm -rf {} +

backend-rebuild: ## Rebuild database inside backend container
	@echo "Rebuilding database inside backend container..."
	docker compose exec -T backend sh -lc 'python -m backend.scripts rebuild-with-export'

backend-rebuild-no-export: ## Rebuild database inside backend container (No export)
	@echo "Rebuilding database inside backend container..."
	docker compose exec -T backend sh -lc 'python -m backend.scripts rebuild'

# Composite tasks
reset-data: clean-uploads backend-rebuild ## Clear uploads and rebuild database in backend container

reset-database: backend-rebuild ## Rebuild database only (uploads unchanged)

# Database maintenance
db-backup: ## Create compressed DB backup (override destination with BACKUP_DIR=/path)
	@echo "Creating DB backup..."
	@sh -c 'set -a; [ -f .env ] && . ./.env; set +a; \
	BACKUP_DIR=$${BACKUP_DIR:-/var/backups/tds-admin/db}; \
	[ -d "$$BACKUP_DIR" ] || sudo mkdir -p "$$BACKUP_DIR"; \
	sudo env BACKUP_DIR="$$BACKUP_DIR" bash scripts/db_backup.sh'

db-restore: ## Restore DB from FILE=<path to .sql or .sql.gz>
	@if [ -z "$(FILE)" ]; then echo "Usage: make db-restore FILE=/path/to/backup.sql[.gz]"; exit 1; fi
	@sh -c 'set -a; [ -f .env ] && . ./.env; set +a; \
	if echo "$(FILE)" | grep -qE "\\.gz$$"; then \
	  gunzip -c "$(FILE)"; \
	else \
	  cat "$(FILE)"; \
	fi | docker compose exec -T postgres psql -U "$${POSTGRES_USER:-admin}" -d "$${POSTGRES_DB:-admin}"

# Production deployment targets
prod-start: ## Start production environment with nginx proxy
	@echo "Starting production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d
	@echo "✅ Production environment started!"
	@echo "🌐 App accessible via nginx proxy"

prod-stop: ## Stop production environment and cleanup ports
	@echo "Stopping production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.production.yml down
	@if [ -f "scripts/cleanup-ports.sh" ]; then \
		./scripts/cleanup-ports.sh; \
		echo "✅ Ports released"; \
	fi
	@echo "✅ Production environment stopped!"

prod-restart: ## Restart production environment
	@echo "Restarting production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.production.yml restart
	@echo "✅ Production environment restarted!"

prod-logs: ## Show logs for production services
	@echo "Showing production logs..."
	docker-compose -f docker-compose.yml -f docker-compose.production.yml logs -f

prod-status: ## Show status of production services
	@echo "Production service status:"
	docker-compose -f docker-compose.yml -f docker-compose.production.yml ps

