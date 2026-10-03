# CampusOS

CampusOS is a production-oriented campus intelligence platform built as a modular monolith with a React/TypeScript frontend, FastAPI API, PostgreSQL, Redis, Celery, structured logging, Prometheus metrics, and explicit data/ML pipelines.

The current verified slice includes JWT authentication, backend-enforced roles, an API-backed student workspace, attendance intelligence, academics and marks, content-based event recommendations, smart complaint intake, campus locations, notifications, a tool-grounded assistant, ML inference, WebSockets, audit records, ETL validation, monitoring, seed data, and CI foundations.

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

- Product UI: http://localhost:3000
- API documentation: http://localhost:8000/api/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (`admin` / `campusos`)

Demo accounts are created on first start:

| Role | Email | Password |
|---|---|---|
| Student | student@campusos.local | Student123! |
| Faculty | faculty@campusos.local | Faculty123! |
| Admin | admin@campusos.local | Admin123! |
| Maintenance | maintenance@campusos.local | Maintain123! |

## Development

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DATABASE_URL=sqlite:///./campusos.db JWT_SECRET=local-development-secret-with-32-chars python -m app.seed
DATABASE_URL=sqlite:///./campusos.db JWT_SECRET=local-development-secret-with-32-chars uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Verification:

```bash
cd backend && .venv/bin/pytest -q
cd frontend && npm run lint && npm test
```

See `docs/` for architecture, API, database, ML/RAG, and deployment notes. External LLM use is optional; the local assistant uses deterministic, authenticated tools and does not invent database values.
