FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire workspace into the container
COPY . .

# Ensure logs and telemetry directories exist
RUN mkdir -p logs/telemetry engine

# Default command runs the ControlArena protocol test wrapper
CMD ["PYTHONPATH=.", "python3", "engine/test_protocol.py"]
