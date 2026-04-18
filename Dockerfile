# --- Builder ---
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear un entorno virtual para que sea fácil de mover
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.prod.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.prod.txt

# --- Producción ---
FROM python:3.12-slim

# Evitar variables repetitivas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Crear usuario y directorios en un solo paso
RUN useradd -m -r appuser && \
    mkdir /app && \
    chown appuser:appuser /app

# Instalar librerías de ejecución si son necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar el entorno virtual completo desde el builder
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# Copiar solo el código de la aplicación
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8765

CMD ["gunicorn", "--bind", "0.0.0.0:8765", "miau_backend.wsgi:application"]