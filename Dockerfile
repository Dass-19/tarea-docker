FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY requirements.txt .

RUN uv pip install --system --no-cache -r requirements.txt

RUN useradd --create-home appuser

COPY --chown=appuser:appuser data/ data/
COPY --chown=appuser:appuser transform.py .

ENV INPUT_PATH=/app/data/raw/data.csv \
    OUTPUT_PATH=/app/data/processed/data.csv

USER appuser

CMD ["python", "transform.py"]
