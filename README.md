# TDS Corporate Website

The public-facing corporate website for The Data Supermarket (TDS), featuring the Mobile KYC product.

## Overview

This is a marketing website showcasing TDS's **Mobile KYC & Trust Scoring** product — carrier-derived identity verification and fraud prevention using mobile network signals.

### Key Features

- **Mobile KYC Product Landing Page** (`/mobile-kyc`)
  - Carrier-backed identity verification across UK mobile networks
  - Fraud prevention, lead validation, and risk reduction
  - Integration with major carriers: Vodafone, EE, O2, Three
  - Partnership with Prove for identity verification

### Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15.5, React 19, TypeScript |
| Backend | FastAPI (Python 3.13), SQLAlchemy |
| Database | PostgreSQL 17 |
| Infrastructure | Docker Compose, Nginx |

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd tds-corporate
   ```

2. **Set up environment variables:**
   ```bash
   cp env.local .env
   # Edit .env with your actual values
   ```

3. **Start the full stack:**
   ```bash
   docker compose up -d
   ```

4. **Access your application:**
   - **Website**: http://localhost:3000
   - **Mobile KYC Page**: http://localhost:3000/mobile-kyc
   - **API Documentation**: http://localhost:9999/docs

### Development Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Rebuild after changes
docker compose up -d --build

# Stop services
docker compose down
```

### Optional: SSL for Local Development

```bash
# Create SSL directory and generate self-signed certificates
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -subj "/CN=localhost"

# Start with nginx profile
docker compose --profile nginx up -d
```

## Project Structure

```
tds-corporate/
├── frontend/               # Next.js application
│   └── src/
│       ├── app/
│       │   ├── page.tsx           # Homepage
│       │   ├── mobile-kyc/        # Mobile KYC landing page
│       │   └── product/           # Product page
│       ├── components/            # Reusable components
│       └── css/                   # Stylesheets
├── backend/                # FastAPI application
│   ├── main.py            # API routes
│   └── models/            # Database models
├── docker/                # Dockerfiles
├── infrastructure/        # Deployment scripts
└── docker-compose.yml     # Service orchestration
```

## Troubleshooting

**SSL Certificate Issues:**
- SSL certificates are only needed when running with nginx profile
- Regenerate if nginx fails to start with SSL errors

**Browser SSL Warnings:**
- Self-signed certificates will show browser warnings (normal for local development)
- Accept the security warning or use HTTP instead

