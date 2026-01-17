# Infrastructure Scripts

This directory contains all infrastructure deployment and management scripts, including reverse proxy configuration and multi-app deployment tools.

## Scripts

### `setup-server-initial.sh`
Initial server bootstrap script that:
- Installs Docker, nginx, certbot, and other required packages
- Creates the 'dev' user with proper permissions
- Configures SSH security settings
- Sets up nginx reverse proxy for multi-app deployment
- Configures firewall rules

**Usage:**
```bash
sudo ./infrastructure/setup-server-initial.sh
```

### `setup-project.sh`
Project deployment script that:
- Prompts for GitHub org, repo, app name, and domain
- Sets up SSH keys for GitHub access
- Clones/updates the repository
- Configures environment variables and secrets
- Sets up SSL certificates (Let's Encrypt)
- Deploys the application in multi-app mode
- Generates nginx configuration

**Usage:**
```bash
./infrastructure/setup-project.sh
```

### `generate-nginx-configs.sh`
Nginx configuration generator that:
- Scans for running Docker containers
- Generates nginx configs for each app
- Updates the reverse proxy configuration
- Reloads nginx

**Usage:**
```bash
sudo ./infrastructure/generate-nginx-configs.sh
```

## Directory Structure

```
infrastructure/
├── README.md
├── DEPLOYMENT.md              # Complete deployment guide
├── setup-server-initial.sh    # Server bootstrap
├── setup-project.sh          # App deployment
├── generate-nginx-configs.sh # Nginx config generator
└── nginx-reverse-proxy.conf  # Reverse proxy template
```

## Usage

These scripts are designed to be run directly from the `infrastructure` directory:

```bash
# Setup server (one-time)
sudo ./infrastructure/setup-server-initial.sh

# Deploy apps
./infrastructure/setup-project.sh
```

This separation keeps infrastructure code separate from application code and makes the scripts easier to maintain and modify.

## Documentation

For complete deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).
