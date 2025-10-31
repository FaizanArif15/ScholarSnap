# Use lightweight Python image
FROM python:3.12.6-slim

# Set working directory
WORKDIR /app

# Avoid Python buffering logs
ENV PYTHONUNBUFFERED=1

# Install system dependencies (needed for building wheels, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock /app/

# Install all dependencies defined in pyproject.toml
RUN uv sync --frozen

# Copy rest of your project
COPY . /app

# Default command (runs your scheduler)
CMD ["uv", "run", "python", "main.py"]
