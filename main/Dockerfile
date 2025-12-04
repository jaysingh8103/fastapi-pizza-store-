# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Install the package
RUN pip install -e .

# Create data directory for database
RUN mkdir -p /app/data

# Set environment variables
ENV DB_PATH=/app/data/pizza_store.sqlite
ENV PYTHONUNBUFFERED=1

# Initialize database
RUN python -c "from main.database import initialize_database; initialize_database()"

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main.api:app", "--host", "0.0.0.0", "--port", "8000"]