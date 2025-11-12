FROM python:3.12.6
WORKDIR /app

COPY . /app
# COPY pyproject.toml uv.lock /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential ca-certificates supervisor \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"

RUN uv sync --frozen

# Default command: Supervisor starts both Celery worker & beat
CMD ["supervisord", "-c", "supervisord.conf"]
