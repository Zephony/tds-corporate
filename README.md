# TDS Admin Panel

The Admin panel for The Data Supermarket.

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd tds-admin
   ```

2. **Set up environment variables:**
   ```bash
   cp env.local .env
   # Edit .env with your actual values
   ```
   Tip: Ask a colleague for the initial `.env` setup.

3. **(Optional) Generate SSL certificates for local development:**
   ```bash
   # Create SSL directory and generate self-signed certificates
   mkdir -p ssl
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout ssl/key.pem \
     -out ssl/cert.pem \
     -subj "/C=US/ST=State/L=City/O=City/O=Organization/CN=City/O=Organization/CN=localhost"
   ```
   
   **Note**: The `ssl/` directory is gitignored for security reasons. Each developer needs to generate their own certificates locally.

4. **Start the full stack:**
   ```bash
   # Start services without nginx (default development setup)
   docker compose up -d
   
   # To start with nginx (production-like setup)
   docker compose --profile nginx up -d
   ```

5. **Reset the database (initial setup):**
   ```bash
   make reset-database
   ```

   Extra tip: To also clear uploaded files used during development/testing, run:
   ```bash
   make reset-data
   ```

6. **Access your application:**

   **Without nginx (default):**
   - **Next.js app**: http://localhost:3000
   - **API Documentation**: http://localhost:9999/docs

   **With nginx (production-like):**
   - **Next.js app**: http://localhost (if enabled)
   - **API Documentation**: http://localhost/api/docs

### Troubleshooting

**SSL Certificate Issues:**
- SSL certificates are only needed when running with nginx profile
- If nginx fails to start with SSL errors, regenerate the certificates:
  ```bash
  rm -rf ssl/
  mkdir -p ssl
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=City/O=City/O=City/O=Organization/CN=localhost"
  ```

**Browser SSL Warnings:**
- Self-signed certificates will show browser warnings (normal for local development)
- Accept the security warning or use HTTP instead of HTTPS

