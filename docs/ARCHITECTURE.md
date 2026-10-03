# CampusOS architecture

CampusOS begins as a modular monolith: one deployable FastAPI application with explicit service and repository boundaries, plus independent Celery workers. This avoids premature network boundaries while keeping attendance, complaints, recommendations, AI, analytics, and notifications separable.

```text
React client -> FastAPI API -> application services -> repositories -> PostgreSQL
                      |                |
                      |                +-> model inference
                      +-> domain events -> Redis -> Celery workers
Operational PostgreSQL -> validated ETL -> analytics/features -> dashboards
Documents -> validation/extraction -> chunks/metadata -> pgvector -> retrieval -> cited LLM answer
```

## Security boundaries

JWT access tokens are short-lived. Refresh tokens are separately typed. Every route enforces roles in the backend. Student-owned resources must be scoped by the authenticated user. SQLAlchemy parameterization prevents direct SQL interpolation. Upload and AI modules should validate size/type, redact secrets, and record auditable actions.

## Event flow

Domain actions emit named events such as `AttendanceUpdated` and `ComplaintCreated`. Redis transports events; Celery consumers recalculate risks, create notifications, and refresh analytics. Failed tasks retry with exponential backoff and remain observable through structured logs.

## ML lifecycle

Training is offline. Validated datasets move through preprocessing, feature engineering, train/validation splits, evaluation, and artifact registration. The API loads versioned artifacts once and records predictions, versions, probabilities, and explainable contributing factors. Predictions support human decisions; they do not replace them.

## Implemented boundaries

The React workspace authenticates against FastAPI and loads one user-scoped dashboard aggregate. Attendance calculations live in the attendance service; recommendation ranking lives in its own service; complaint classification and audit creation are transactional; assistant intents call authenticated application tools. The browser never supplies a student identity for personal records.

## Next increments

Faculty/admin/maintenance screens, durable event registration, document upload and pgvector ingestion, trained ML artifacts with MLflow, email delivery, and deeper analytics remain explicit later phases rather than simulated frontend features.
