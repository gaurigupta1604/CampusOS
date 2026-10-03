FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -r -u 10001 campusos && chown -R campusos:campusos /app
USER campusos
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
