FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only the TraceGuard Core package and its declared runtime dependencies.
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN python -m pip install --no-cache-dir .

# Run the decision-only MCP server over stdio.
CMD ["traceguard-core"]
