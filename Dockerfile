FROM python:3.12-slim

WORKDIR /app

COPY webServer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webServer/ ./webServer/

WORKDIR /app/webServer
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
