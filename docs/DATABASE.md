# Database

PostgreSQL is the primary store. SQLAlchemy models cover users, departments, students, faculty, courses, enrollments, attendance, assignments, marks, events, clubs, complaints, notifications, audits, and model predictions. Foreign keys, unique constraints, and indexes protect common integrity and lookup paths.

`python -m app.seed` is idempotent for the demo workspace and enhances an older seed with assignments, marks, notifications, and a complaint. Schema evolution should use Alembic migrations before production deployment.
