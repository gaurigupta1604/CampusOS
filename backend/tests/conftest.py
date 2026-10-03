import os
os.environ["DATABASE_URL"]="sqlite:///./test.db"
os.environ["JWT_SECRET"]="test-secret-key-with-more-than-32-characters"
import pytest
from fastapi.testclient import TestClient
from app.core.database import Base,SessionLocal,engine
from app.core.security import hash_password
from app.main import app
from app.models.domain import Role,User
@pytest.fixture(autouse=True)
def database():
    Base.metadata.drop_all(engine);Base.metadata.create_all(engine)
    with SessionLocal() as db:
        db.add(User(email="student@test.edu",full_name="Test Student",password_hash=hash_password("Student123!"),role=Role.STUDENT));db.commit()
    yield
    Base.metadata.drop_all(engine)
@pytest.fixture
def client():return TestClient(app)
