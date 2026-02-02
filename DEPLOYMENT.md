# TDS Corporate Deployment Guide

This guide will walk you through deploying the TDS Corporate website to DigitalOcean using GitHub Actions for automated deployments.

## Prerequisites

- DigitalOcean account
- GitHub repository with your code
- Domain name (optional but recommended)
- SSH key pair

## Step 1: Set Up DigitalOcean Droplet

### 1.1 Create a Droplet
1. Log into your DigitalOcean account
2. Click "Create" → "Droplets"
3. Choose "Ubuntu 22.04 LTS" as the image
4. Select a plan (recommended: Basic plan with 2GB RAM minimum)
5. Choose a datacenter region close to your users
6. Add your SSH key
7. Click "Create Droplet"

### 1.2 Connect to Your Droplet
```bash
ssh root@YOUR_DROPLET_IP
```

### 1.3 Create a Non-Root User
```bash
# Create a new user
adduser deploy
usermod -aG sudo deploy

# Switch to the new user
su - deploy
```

## Step 2: Initial Server Setup

### 2.1 Run the Server Setup Script
```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/tds-corporate.git
cd tds-corporate

# Run the server setup script
./setup-server.sh
```

**Note**: The script will install Docker, Docker Compose, and set up the basic server configuration. You may need to log out and back in after Docker installation.

### 2.2 Verify Installation
```bash
# Check if services are running
docker-compose ps

# Check logs if needed
docker-compose logs -f
```

## Step 3: Set Up GitHub Actions

### 3.1 Add Repository Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions, and add:

- `DROPLET_HOST`: Your droplet's IP address
- `DROPLET_USERNAME`: The username you created (e.g., 'deploy')
- `DROPLET_SSH_KEY`: Your private SSH key content
- `DOMAIN`: Your domain name (if you have one)

### 3.2 Set Up SSH Key
1. Generate an SSH key pair if you don't have one: `ssh-keygen -t rsa -b 4096`
2. Copy your public key to the droplet: `ssh-copy-id deploy@YOUR_DROPLET_IP`
3. Add your private key content to GitHub secrets as `DROPLET_SSH_KEY`

### 3.3 Test SSH Connection
```bash
# Test SSH connection to your droplet
ssh deploy@YOUR_DROPLET_IP

# If successful, you're ready for automated deployments
```

## Step 4: Configure Domain and SSL (Optional)

### 4.1 Point Domain to Your Droplet
1. Go to your domain registrar's DNS settings
2. Add an A record pointing to your droplet's IP address
3. Wait for DNS propagation (can take up to 48 hours)

### 4.2 Set Up Let's Encrypt SSL
```bash
# Install Certbot
sudo apt install certbot

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates to the application directory
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/tds-corporate/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/tds-corporate/ssl/key.pem

# Set proper permissions
sudo chown deploy:deploy /opt/tds-corporate/ssl/*
sudo chmod 600 /opt/tds-corporate/ssl/*

# Restart services
cd /opt/tds-corporate
docker-compose restart nginx
```

### 4.3 Update Environment Variables
```bash
# Edit the .env file
nano /opt/tds-corporate/.env

# Update these values:
NEXT_PUBLIC_API_URL=https://your-domain.com/api
ALLOWED_HOSTS=your-domain.com
```

## Step 5: Test Deployment

### 5.1 Manual Test
```bash
# Test the API
curl https://your-domain.com/api/v1/health

# Test the root route
curl https://your-domain.com/
```

### 5.2 Automated Deployment Test
1. Make a small change to your code
2. Push to the main branch
3. Check GitHub Actions to see the deployment
4. Verify the changes are live on your server

## Step 6: Monitoring and Maintenance

### 6.1 View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

### 6.2 Update Services
```bash
cd /opt/tds-corporate
docker-compose pull
docker-compose up -d
```

### 6.3 Backup Database
PostgreSQL is bound to localhost and not exposed publicly. Use the bundled script (defaults to `/var/backups/tds-corporate/db`, override with `BACKUP_DIR`):
```bash
# One-off backup (compressed) to backups/db/
bash scripts/db_backup.sh

# Restore (example)
gunzip -c backups/db/<dbname>_YYYYMMDD_HHMMSS.sql.gz | docker compose exec -T postgres psql -U ${POSTGRES_USER:-admin} -d ${POSTGRES_DB:-admin}
```
You can optionally install a daily cron during `setup-project.sh`.

## Troubleshooting

### Common Issues

#### 1. Services Not Starting
```bash
# Check service status
docker-compose ps

# Check logs
docker-compose logs [service_name]

# Restart services
docker-compose restart
```

#### 2. Port Conflicts
```bash
# Check what's using the ports
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Stop conflicting services
sudo systemctl stop apache2  # if Apache is running
sudo systemctl stop nginx    # if system nginx is running
```

#### 3. Permission Issues
```bash
# Fix file permissions
sudo chown -R deploy:deploy /opt/tds-corporate
chmod 600 /opt/tds-corporate/.env
chmod 600 /opt/tds-corporate/ssl/*
```

#### 4. Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose exec postgres pg_isready -U admin

# Check database logs
docker-compose logs postgres
```

## Security Considerations

1. **Firewall**: Configure UFW to only allow necessary ports
2. **SSH**: Use key-based authentication only
3. **Updates**: Regularly update your droplet and Docker images
4. **Backups**: Set up automated database backups
5. **Monitoring**: Consider setting up monitoring and alerting

## Performance Optimization

1. **Database**: Consider using connection pooling
2. **Caching**: Implement Redis for session storage
3. **CDN**: Use a CDN for static assets
4. **Load Balancing**: Set up multiple droplets behind a load balancer for high availability

## Support

If you encounter issues:
1. Check the logs: `docker compose logs -f`
2. Verify environment variables are set correctly
3. Ensure all required ports are open
4. Check GitHub Actions logs for deployment issues

## Next Steps

After successful deployment:
1. Set up monitoring and alerting
2. Configure automated backups
3. Set up CI/CD pipeline for testing
4. Implement logging and analytics
5. Plan for scaling and high availability

