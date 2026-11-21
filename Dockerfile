FROM python:3.14-slim

LABEL org.opencontainers.image.title="Monitor APP-06 - Recetas Rápidas" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.source="https://github.com/fregona33/monitor-app-06"

WORKDIR /app

COPY monitor_app.py .

CMD ["python", "monitor_app.py"]