FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (good for psycopg / geo libs if needed)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    libpq-dev \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock* ./

# Install deps
RUN uv sync --frozen

# Copy rest of app
COPY . .

EXPOSE 8000
ENV PYTHONPATH=/app

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
