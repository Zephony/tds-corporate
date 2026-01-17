FROM node:22-bookworm-slim AS base
WORKDIR /app

# Install dependencies only when needed
FROM base AS deps
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --only=production && npm cache clean --force

# Development stage
FROM base AS dev
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1
EXPOSE 8081
CMD ["npm", "run", "dev"]

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY frontend/ .

# Disable ESLint and type checking in production builds
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
ENV ESLINT_NO_DEV_ERRORS=true
ENV NEXT_IGNORE_ESLINT_ERRORS=true
ENV NEXT_IGNORE_TYPE_ERRORS=true

RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=8081
ENV HOSTNAME=0.0.0.0

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Copy the full .next build including static files
COPY --from=builder /app/.next ./.next
RUN chown -R nextjs:nodejs .next
COPY --from=builder /app/package.json ./package.json

# Install only runtime dependencies
RUN npm install next react react-dom --production --no-audit --no-fund

# Create a simple startup script that handles both standalone and regular builds
RUN echo '#!/bin/sh\nset -e\nif [ -f .next/standalone/server.js ]; then\n  exec node .next/standalone/server.js\nelse\n  exec npx next start -p $PORT -H $HOSTNAME\nfi' > /start.sh && chmod +x /start.sh

USER nextjs

EXPOSE 8081

CMD ["/start.sh"]

