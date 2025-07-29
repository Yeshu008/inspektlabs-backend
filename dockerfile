FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

RUN chmod +x wait-for-db.sh

# Expose Flask port (optional)
EXPOSE 5000

# Default command (can be overridden in docker-compose)
CMD ["flask", "run", "--host=0.0.0.0"]
