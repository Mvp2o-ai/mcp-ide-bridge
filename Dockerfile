FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml ./
COPY src/ ./src/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd --create-home --shell /bin/bash mcp
RUN chown -R mcp:mcp /app
USER mcp

# Expose port
EXPOSE 8111

# Set environment variables
ENV MCP_SERVER_HOST=0.0.0.0
ENV MCP_SERVER_PORT=8111
ENV LOG_LEVEL=INFO

# Health check using MCP endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -X POST -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
         -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' \
         http://localhost:8111/mcp/ | grep -q '"tools"' || exit 1

# Run the server
CMD ["python", "-m", "mcp_messaging.server", "--host", "0.0.0.0", "--port", "8111"] 