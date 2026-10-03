# API

The FastAPI schema is available at `http://localhost:8000/api/docs`.

Core routes:

- `POST /api/v1/auth/login` and `/refresh` issue typed JWT pairs.
- `GET /api/v1/campus/dashboard` returns the authenticated student's aggregate workspace.
- `POST /api/v1/campus/assistant` selects a campus tool and returns its sources.
- `GET /api/v1/attendance/students/{student_id}/courses/{course_id}/insight` returns calculated attendance risk.
- `GET|POST /api/v1/complaints` lists or creates user-scoped service requests.
- `GET /api/v1/events/recommended` ranks real event records.
- `POST /api/v1/ml/attendance-risk` is restricted to faculty and administrators.

All personal routes require `Authorization: Bearer <access-token>` and enforce ownership or role permissions in the API.
