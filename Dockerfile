# =============================================================================
# Skizoh Crypto Grid Trading Bot - Optimized Docker Image
# Multi-stage build for Raspberry Pi (ARM64/ARM32)
# =============================================================================
# Optimizations:
# - Multi-stage build reduces image size by ~60%
# - Pre-compiled wheels for ARM
# - Minimal runtime dependencies
# - Non-root user for security
# - Health checks and proper signal handling
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder - Compile dependencies
# -----------------------------------------------------------------------------
FROM python:3.11-slim-bookworm AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install wheel
RUN pip install --no-cache-dir --upgrade pip wheel

# Copy requirements and install dependencies
COPY requirements.txt .

# Install with optimizations for ARM
# --prefer-binary: Use pre-compiled wheels when available
# --no-cache-dir: Don't cache pip packages (smaller image)
RUN pip install --no-cache-dir --prefer-binary \
    -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Runtime - Minimal production image
# -----------------------------------------------------------------------------
FROM python:3.11-slim-bookworm AS runtime

# Labels
LABEL maintainer="Skizoh"
LABEL version="14.2"
LABEL description="Smart Grid Trading Bot for Binance.US - Pi Optimized"

# Environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=2 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=UTC \
    # Reduce numpy thread usage for single-core efficiency
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    VECLIB_MAXIMUM_THREADS=1 \
    NUMEXPR_NUM_THREADS=1

# Install only runtime dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Required for proper signal handling
    tini \
    # Required for health checks
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoremove -y

# Create non-root user for security
RUN groupadd -r gridbot && useradd -r -g gridbot -d /app -s /sbin/nologin gridbot

# Create application directories with proper permissions
RUN mkdir -p /app/src/priv /app/data \
    && chown -R gridbot:gridbot /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application source code
COPY --chown=gridbot:gridbot src/ /app/src/

# Copy entrypoint script
COPY --chown=gridbot:gridbot docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Switch to non-root user
USER gridbot

# Data volume for persistence
VOLUME ["/app/data", "/app/src/priv"]

# Health check - lightweight Python import test
# Interval: 120s (reduced frequency for Pi)
# Timeout: 15s (increased for slower Pi)
# Start-period: 60s (allow initialization time)
HEALTHCHECK --interval=120s --timeout=15s --start-period=60s --retries=3 \
    CMD python3 -c "import ccxt; import numpy; print('ok')" || exit 1

# Use tini as init for proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--", "/app/docker-entrypoint.sh"]

# Default command
CMD ["run"]
