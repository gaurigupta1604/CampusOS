from datetime import date
from app.core.database import SessionLocal
from app.models.domain import AttendanceRecord,Course,Department,Enrollment,Student,User
def student_token(client):return client.post("/api/v1/auth/login",json={"email":"student@test.edu","password":"Student123!"}).json()["access_token"]
def seed_student():
    with SessionLocal() as db:
        user=db.query(User).filter_by(email="student@test.edu").one();department=Department(code="CSE",name="Computer Science");db.add(department);db.flush();student=Student(user_id=user.id,department_id=department.id,registration_number="TEST001",semester=4);db.add(student);db.flush();course=Course(code="CS401",title="Computer Networks",department_id=department.id);db.add(course);db.flush();db.add(Enrollment(student_id=student.id,course_id=course.id,semester=4));db.add(AttendanceRecord(student_id=student.id,course_id=course.id,session_date=date(2026,1,1),present=True));db.commit()
def test_dashboard_uses_authenticated_student_records(client):
    seed_student();response=client.get("/api/v1/campus/dashboard",headers={"Authorization":f"Bearer {student_token(client)}"});assert response.status_code==200;assert response.json()["courses"][0]["code"]=="CS401";assert response.json()["attendance"][0]["current_attendance"]==100
def test_assistant_calls_attendance_tool(client):
    seed_student();response=client.post("/api/v1/campus/assistant",json={"message":"How is my attendance?"},headers={"Authorization":f"Bearer {student_token(client)}"});assert response.status_code==200;assert response.json()["tool"]=="get_attendance"
