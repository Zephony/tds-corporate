FROM python:3.13-slim AS base
# libpangocairo is required for WeasyPrint
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Development stage
FROM base AS dev
ARG REQUIREMENTS_FILE=requirements-dev.txt
COPY ${REQUIREMENTS_FILE} /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . .
EXPOSE 9999
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "9999", "--reload"]

# Production stage
FROM base AS prod
ARG REQUIREMENTS_FILE=requirements.txt
COPY ${REQUIREMENTS_FILE} /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . .
EXPOSE 9999
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "9999"]
