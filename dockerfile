FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including pip
RUN apt-get update && apt-get install -y \
    curl python3-pip libsnappy-dev make gcc g++ libc6-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using pip instead of uv (fallback)
RUN pip install -e .

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]