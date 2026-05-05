FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "app.cli", "serve-demo", "--host", "0.0.0.0", "--port", "5000"]
