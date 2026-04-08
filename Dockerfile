# ─── BUILD ────────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Dependências de sistema (necessárias para psycopg2 e Pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ─── PRODUÇÃO ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Dependências de runtime (libpq para psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar packages instalados do builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código do projeto
COPY . .

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Usuário não-root por segurança
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Cloud Run injeta $PORT — gunicorn escuta nela
CMD exec gunicorn adfidelidade.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 120
