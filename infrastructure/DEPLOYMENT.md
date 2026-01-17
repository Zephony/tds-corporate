# Multi-App Deployment Guide

This guide explains how to deploy multiple applications on the same server using a reverse proxy architecture.

## Overview

This deployment strategy solves common multi-app server problems:
- **Port Conflicts**: Only reverse proxy uses ports 80/443
- **Container Name Conflicts**: Each app uses project-specific names
- **Volume Conflicts**: Each app gets isolated databases
- **Network Conflicts**: Apps communicate internally only

## Architecture

```
Internet → Host Nginx (Ports 80/443) → App 1 Nginx → App 1 Backend
                                → App 2 Nginx → App 2 Backend
                                → App 3 Nginx → App 3 Backend
```

## Quick Start

### 1. Setup Server (One-time)

```bash
# On your server
sudo ./infrastructure/setup-server-initial.sh
```

This installs Docker, nginx, certbot, and configures the reverse proxy.

### 2. Deploy Apps

```bash
# Deploy first app
./infrastructure/setup-project.sh

# Deploy additional apps
cd /path/to/another-app
./infrastructure/setup-project.sh
```

Each app is automatically deployed with isolated containers and no external ports.

## Detailed Setup

### Prerequisites

- Ubuntu 22.04+ server
- Root or sudo access
- Domain name (optional)
- GitHub repository

### Server Setup

The `setup-server-initial.sh` script:

1. **Installs Dependencies**:
   - Docker and Docker Compose
   - nginx and certbot
   - Required system packages

2. **Creates User**:
   - Creates 'dev' user with sudo access
   - Sets up SSH key authentication
   - Configures fish shell

3. **Configures Security**:
   - Sets up UFW firewall
   - Hardens SSH configuration
   - Disables root login

4. **Sets up Reverse Proxy**:
   - Configures nginx for multi-app routing
   - Creates conf.d directory for app configs
   - Starts nginx service

### App Deployment

The `setup-project.sh` script for each app:

1. **Collects Information**:
   - GitHub org/repo details
   - App name and domain
   - Backup preferences

2. **Sets up Repository**:
   - Generates SSH keys for GitHub
   - Clones/updates repository
   - Sets up proper permissions

3. **Configures Environment**:
   - Generates secure passwords
   - Sets up domain configuration
   - Creates SSL certificates

4. **Deploys Application**:
   - Uses production Docker Compose config
   - Generates nginx configuration
   - Starts all services

## File Structure

```
/var/www/
├── goods-keeper/           # App 1
│   ├── docker-compose.yml
│   ├── docker-compose.production.yml
│   └── infrastructure/
│       ├── setup-server-initial.sh
│       ├── setup-project.sh
│       └── generate-nginx-configs.sh
├── another-app/            # App 2
│   ├── docker-compose.yml
│   ├── docker-compose.production.yml
│   └── infrastructure/
│       └── [same scripts]
└── /etc/letsencrypt/live/  # Let's Encrypt certificates
    ├── app.example.com/
    │   ├── fullchain.pem
    │   └── privkey.pem
    └── app2.example.com/
        ├── fullchain.pem
        └── privkey.pem
```

## Docker Compose Configuration

### Development
```bash
docker-compose up -d  # Uses external ports
```

### Production (Multi-app)
```bash
docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d
```

The production override:
- Removes external port mappings
- Sets production environment variables
- Uses production build targets
- Enables restart policies

## Environment Variables

Each app needs these in `.env`:

```bash
# Domain configuration
DOMAIN=app.example.com
ALLOWED_HOSTS=app.example.com,www.app.example.com
NEXT_PUBLIC_API_URL=https://app.example.com/api

# Database
POSTGRES_PASSWORD=secure_random_password
POSTGRES_USER=admin
POSTGRES_DB=app_name

# Security
SECRET_KEY=very_long_random_secret_key
```

## SSL Certificate Management

### Automatic (Recommended)
The setup script automatically:
1. Uses Let's Encrypt certificates for host nginx
2. Stores certificates in standard `/etc/letsencrypt/live/` directory
3. Only HTTPS works if certificates are successfully installed

### Manual
```bash
# Install certificates manually using certbot
sudo certbot certonly --standalone -d app.example.com

# Regenerate nginx configs
sudo ./infrastructure/generate-nginx-configs.sh
```

## Management Commands

### View Running Apps
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### View App Logs
```bash
# Specific app
cd /var/www/app-name
docker-compose -f docker-compose.yml -f docker-compose.production.yml logs -f

# Reverse proxy
sudo journalctl -u nginx -f
```

### Restart App
```bash
cd /var/www/app-name
docker-compose -f docker-compose.yml -f docker-compose.production.yml restart
```

### Update App
```bash
cd /var/www/app-name
git pull
docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d --build
```

### Regenerate Nginx Config
```bash
sudo ./infrastructure/generate-nginx-configs.sh
```

## Troubleshooting

### Port Conflicts
```bash
# Check what's using ports
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Stop conflicting services
sudo systemctl stop apache2
sudo systemctl stop nginx
```

### Container Issues
```bash
# Check container status
docker ps -a

# View container logs
docker logs container-name

# Restart specific service
docker-compose restart service-name
```

### Nginx Issues
```bash
# Test configuration
sudo nginx -t

# Reload configuration
sudo systemctl reload nginx

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### SSL Issues
```bash
# Check certificates
sudo certbot certificates

# Renew certificates
sudo certbot renew

# Test SSL
openssl s_client -connect domain.com:443
```

## Security Best Practices

1. **Firewall**: Only open ports 22, 80, 443
2. **SSH**: Use key-based authentication only
3. **Updates**: Keep system and Docker images updated
4. **Monitoring**: Set up log monitoring and alerts
5. **Backups**: Regular database and file backups
6. **SSL**: Use Let's Encrypt for production domains

## Performance Optimization

1. **Nginx Caching**: Configure static asset caching
2. **Database**: Use connection pooling
3. **CDN**: Use CDN for static assets
4. **Monitoring**: Set up resource monitoring

## Scaling

### Horizontal (Multiple Servers)
1. Set up load balancer
2. Deploy same setup on each server
3. Configure DNS to point to load balancer

### Vertical (Same Server)
1. Increase server resources
2. Optimize container resource limits
3. Use Docker Swarm or Kubernetes

## Migration from Single-App

1. **Backup Data**:
   ```bash
   # Database
   docker-compose exec postgres pg_dump -U admin admin > backup.sql
   
   # Files
   tar -czf app-backup.tar.gz uploads/ files/ static/
   ```

2. **Deploy Multi-App**:
   ```bash
   ./infrastructure/setup-project.sh
   ```

3. **Restore Data**:
   ```bash
   # Database
   docker-compose -f docker-compose.yml -f docker-compose.production.yml exec -T postgres psql -U admin admin < backup.sql
   
   # Files
   tar -xzf app-backup.tar.gz
   ```

## Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify nginx: `sudo nginx -t`
3. Check containers: `docker ps`
4. Verify SSL: `sudo certbot certificates`
5. Check firewall: `sudo ufw status`

## Next Steps

After successful deployment:

1. Set up monitoring and alerting
2. Configure automated backups
3. Set up CI/CD pipeline
4. Implement logging and analytics
5. Plan for scaling and high availability
