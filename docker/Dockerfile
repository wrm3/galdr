# galdr - Unified MCP Server
# Combines RAG, Research, MediaWiki, Oracle, Template Installation, and Video Analysis

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# - git: required for some pip installs
# - libaio1t64: required for Oracle Instant Client thick mode
# - unzip: for extracting Oracle Instant Client
# - ffmpeg: for video frame extraction
# - libgl1, libglib2.0-0: for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    curl \
    git \
    unzip \
    libaio1t64 \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Debian Trixie renamed libaio.so.1 -> libaio.so.1t64 (64-bit time_t transition)
# Oracle Instant Client requires the old name, so create a compat symlink
RUN ln -sf /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1 \
    && ldconfig

# ============================================================
# Oracle Instant Client 23.x (thick mode for Network Encryption)
# ============================================================
RUN mkdir -p /opt/oracle && \
    curl -fSL https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linuxx64.zip \
         -o /tmp/instantclient-basic.zip && \
    unzip -q /tmp/instantclient-basic.zip -d /opt/oracle && \
    rm /tmp/instantclient-basic.zip && \
    ln -s /opt/oracle/instantclient_* /opt/oracle/instantclient && \
    echo /opt/oracle/instantclient > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

# Oracle environment variables
ENV ORACLE_HOME=/opt/oracle/instantclient
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient:${LD_LIBRARY_PATH}

# Copy requirements first for better caching
COPY docker/requirements.txt docker/pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install crawl4ai for server-side documentation crawling
RUN pip install --no-cache-dir crawl4ai && \
    python -m crawl4ai.install || true

# Copy DB init scripts (run at startup if schema is missing)
COPY docker/init_db/*.sql ./init_db/

# Copy application code
COPY docker/galdr/ ./galdr/

# Copy video analyzer package (used by galdr video plugins via lazy import)
COPY docker/galdr_video_analyzer/ ./galdr_video_analyzer/

# Bake templates/ into the image so galdr_install can serve it without GitHub calls
# The install_rest endpoint zips this directory on demand and streams it to the caller
COPY templates/ ./templates/

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/research_output /app/cache /app/frames

# Environment variables (can be overridden)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LOG_LEVEL=INFO

# Copy entrypoint (runs DB init if schema missing, then starts server)
COPY docker/entrypoint.sh ./entrypoint.sh
RUN sed -i 's/\r$//' ./entrypoint.sh && chmod +x ./entrypoint.sh

# Expose port for HTTP/SSE transport
EXPOSE 8092

# Entrypoint: init DB schema if needed, then start MCP server
ENTRYPOINT ["./entrypoint.sh"]
