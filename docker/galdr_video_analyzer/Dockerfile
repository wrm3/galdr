# galdr_video_analyzer Docker Image
# YouTube Video Analysis MCP Server with yt-dlp, OpenCV, and Claude Vision

FROM python:3.11-slim

# Install system dependencies
# - ffmpeg: Required for video/audio processing
# - libgl1: Required for OpenCV (libgl1 replaces deprecated libgl1-mesa-glx)
# - curl: For health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
# Note: Build context is ./galdr_video_analyzer, so copy from current dir
COPY . ./galdr_video_analyzer/

# Create directories for data persistence
RUN mkdir -p /app/cache /app/frames /app/logs /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MCP_TRANSPORT=sse \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8084 \
    VIDEO_CACHE_DIR=/app/cache \
    VIDEO_FRAMES_DIR=/app/frames \
    VIDEO_STATE_FILE=/app/data/state.json

# Expose the MCP server port
EXPOSE 8084

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -sf http://localhost:8084/health || exit 0

# Run the server
CMD ["python", "-m", "galdr_video_analyzer.server"]
