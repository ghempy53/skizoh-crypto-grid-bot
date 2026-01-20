# =============================================================================
# Skizoh Crypto Grid Trading Bot - Docker Image
# Optimized for Raspberry Pi (ARM64/ARM32)
# =============================================================================

# Use official Python image - automatically selects ARM variant on Pi
FROM python:3.11-slim-bookworm

# Labels
LABEL maintainer="Skizoh"
LABEL version="14.1"
LABEL description="Smart Grid Trading Bot for Binance.US"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=UTC

# Install system dependencies
# numpy requires some build tools on ARM
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r gridbot && useradd -r -g gridbot gridbot

# Create application directories
RUN mkdir -p /app/src/priv /app/data \
    && chown -R gridbot:gridbot /app

# Set working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY --chown=gridbot:gridbot requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY --chown=gridbot:gridbot src/ /app/src/

# Copy entrypoint script
COPY --chown=gridbot:gridbot docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Switch to non-root user
USER gridbot

# Data volume for persistence (logs, position state, tax records)
VOLUME ["/app/data", "/app/src/priv"]

# Health check - verify Python can import modules
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python3 -c "import ccxt; import numpy; print('healthy')" || exit 1

# Set entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default command
CMD ["run"]
