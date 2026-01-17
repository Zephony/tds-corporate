FROM python:3.13-slim
# libpangocairo is required for WeasyPrint; poppler-utils (pdftoppm) for pdf2image
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential libpangocairo-1.0-0 poppler-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["celery", "-A", "backend.celery_app.celery", "worker", "--loglevel=INFO"]
