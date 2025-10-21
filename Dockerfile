# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv (fast package manager).
RUN pip install --no-cache-dir uv

COPY pyproject.toml README.md /app/
COPY src /app/src

RUN uv pip install --system -e .

EXPOSE 8080
CMD ["mcp-devhatchery"]
