FROM python:3.13-slim@sha256:ffb752e139c0a19692a43af8d8523b274222dd68eebad5d583b45c2201c6e30a

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && adduser --disabled-password --gecos "" --uid 10001 appuser

COPY support_ops ./support_ops
COPY eval_cases.json ./eval_cases.json

USER appuser
ENV PORT=8080 PYTHONUNBUFFERED=1 OTEL_SERVICE_NAME=support-ops
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/docs', timeout=4)" || exit 1

CMD ["sh", "-c", "adk api_server --host 0.0.0.0 --port ${PORT} ."]
