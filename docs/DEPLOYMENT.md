# Deployment and operations

Local development is centred on one VS Code terminal:

```bash
docker compose up --build
```

The stack includes the React frontend, FastAPI, PostgreSQL/pgvector, Redis, Celery worker and beat, Prometheus, and Grafana. Health endpoints and structured request logs are enabled. Replace all development credentials and the JWT secret before any public deployment. Restrict CORS to the deployed frontend origin and use managed secret storage.
