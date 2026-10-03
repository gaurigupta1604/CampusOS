from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import current_user
from app.core.database import get_db
from app.models.domain import (
    Assignment, AttendanceRecord, Complaint, Course, Enrollment, Event, Mark,
    Notification, Student, User,
)
from app.schemas.domain import AssistantRequest, AssistantResponse
from app.services.attendance import AttendanceService
from app.services.recommendations import recommend_events

router = APIRouter(prefix="/campus", tags=["campus"])

LOCATIONS = [
    {"id": 1, "name": "Innovation Block", "type": "Academic", "room": "204", "floor": "Second floor", "hours": "08:00–20:00", "x": 68, "y": 31},
    {"id": 2, "name": "Central Library", "type": "Library", "room": "Help desk", "floor": "Ground floor", "hours": "07:00–22:00", "x": 36, "y": 49},
    {"id": 3, "name": "Technology Centre", "type": "Laboratory", "room": "AI Lab", "floor": "Third floor", "hours": "08:00–19:00", "x": 57, "y": 68},
    {"id": 4, "name": "Student Services", "type": "Office", "room": "S-101", "floor": "First floor", "hours": "09:00–17:00", "x": 24, "y": 72},
]

def student_for(user: User, db: Session) -> Student:
    student = db.query(Student).filter_by(user_id=user.id).first()
    if not student:
        raise HTTPException(403, "This view is available to student accounts")
    return student

@router.get("/me")
def me(user: User = Depends(current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter_by(user_id=user.id).first()
    return {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role.value,
            "student_id": student.id if student else None, "semester": student.semester if student else None,
            "registration_number": student.registration_number if student else None}

@router.get("/dashboard")
def dashboard(user: User = Depends(current_user), db: Session = Depends(get_db)):
    student = student_for(user, db)
    enrollments = list(db.scalars(select(Enrollment).where(Enrollment.student_id == student.id)))
    courses = [db.get(Course, enrollment.course_id) for enrollment in enrollments]
    attendance = []
    for course in courses:
        insight = AttendanceService(db).insight(student.id, course.id)
        attendance.append({"course_id": course.id, "code": course.code, "title": course.title, **insight})
    course_ids = [course.id for course in courses]
    assignments = list(db.scalars(select(Assignment).where(Assignment.course_id.in_(course_ids)).order_by(Assignment.due_at))) if course_ids else []
    marks = list(db.scalars(select(Mark).where(Mark.student_id == student.id)))
    events = list(db.scalars(select(Event).order_by(Event.starts_at).limit(20)))
    recommendations = recommend_events(student.interests, student.skills, events, 5)
    event_by_id = {event.id: event for event in events}
    recommended = [{**item, "starts_at": event_by_id[item["event_id"]].starts_at, "location": event_by_id[item["event_id"]].location} for item in recommendations]
    complaints = list(db.scalars(select(Complaint).where(Complaint.reporter_id == user.id).order_by(Complaint.created_at.desc()).limit(10)))
    notifications = list(db.scalars(select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc()).limit(10)))
    mark_average = round(sum(row.score / row.maximum * 100 for row in marks) / len(marks), 1) if marks else None
    overall = round(sum(item["current_attendance"] for item in attendance) / len(attendance), 1) if attendance else 0
    return {
        "profile": {"full_name": user.full_name, "semester": student.semester, "registration_number": student.registration_number},
        "summary": {"overall_attendance": overall, "academic_average": mark_average, "upcoming_assignments": len(assignments), "open_complaints": sum(row.status.value != "resolved" for row in complaints)},
        "courses": [{"id": course.id, "code": course.code, "title": course.title, "credits": course.credits} for course in courses],
        "attendance": attendance,
        "assignments": [{"id": row.id, "course_id": row.course_id, "title": row.title, "due_at": row.due_at, "max_marks": row.max_marks} for row in assignments],
        "marks": [{"id": row.id, "course_id": row.course_id, "assessment": row.assessment, "score": row.score, "maximum": row.maximum} for row in marks],
        "events": recommended,
        "complaints": [{"id": row.id, "description": row.description, "category": row.category, "location": row.location, "priority": row.priority.value, "status": row.status.value, "created_at": row.created_at} for row in complaints],
        "notifications": [{"id": row.id, "title": row.title, "message": row.message, "priority": row.priority.value, "is_read": row.is_read, "created_at": row.created_at} for row in notifications],
        "locations": LOCATIONS,
        "generated_at": datetime.utcnow(),
    }

@router.get("/locations")
def locations(q: str = "", user: User = Depends(current_user)):
    query = q.strip().lower()
    return [row for row in LOCATIONS if not query or query in f'{row["name"]} {row["type"]} {row["room"]}'.lower()]

@router.post("/assistant", response_model=AssistantResponse)
def assistant(payload: AssistantRequest, user: User = Depends(current_user), db: Session = Depends(get_db)):
    student = student_for(user, db)
    message = payload.message.lower()
    if any(word in message for word in ("attendance", "shortage", "risk")):
        enrollments = list(db.scalars(select(Enrollment).where(Enrollment.student_id == student.id)))
        insights = []
        for enrollment in enrollments:
            course = db.get(Course, enrollment.course_id)
            result = AttendanceService(db).insight(student.id, course.id)
            insights.append((course, result))
        if not insights:
            return AssistantResponse(answer="No attendance records are available yet.", tool="get_attendance", sources=[])
        course, result = min(insights, key=lambda item: item[1]["current_attendance"])
        return AssistantResponse(answer=f'{course.title} is currently {result["current_attendance"]}%. You need {result["classes_needed"]} consecutive classes to reach 75%. Risk is {result["risk_level"]}.', tool="get_attendance", sources=[f"attendance_records:{course.id}"])
    if any(word in message for word in ("event", "club", "hackathon", "meetup")):
        events = list(db.scalars(select(Event).order_by(Event.starts_at).limit(50)))
        ranked = recommend_events(student.interests, student.skills, events, 3)
        answer = "; ".join(f'{row["title"]} ({row["reason"]})' for row in ranked) or "No upcoming events were found."
        return AssistantResponse(answer=answer, tool="search_events", sources=[f'events:{row["event_id"]}' for row in ranked])
    if any(word in message for word in ("room", "where", "library", "lab", "map")):
        matches = [row for row in LOCATIONS if any(token in f'{row["name"]} {row["room"]}'.lower() for token in message.split() if len(token) > 2)]
        place = matches[0] if matches else LOCATIONS[0]
        return AssistantResponse(answer=f'{place["name"]} — {place["room"]}, {place["floor"]}. Open {place["hours"]}.', tool="find_room", sources=[f'campus_location:{place["id"]}'])
    if any(word in message for word in ("complaint", "ticket", "issue")):
        rows = list(db.scalars(select(Complaint).where(Complaint.reporter_id == user.id).order_by(Complaint.created_at.desc()).limit(3)))
        answer = "; ".join(f'#{row.id} {row.category}: {row.status.value}' for row in rows) or "You have no complaints on record."
        return AssistantResponse(answer=answer, tool="get_complaints", sources=[f"complaints:{row.id}" for row in rows])
    return AssistantResponse(answer="I can use your live CampusOS records for attendance, events, campus locations, and complaints. Ask me one of those questions.", tool="capabilities", sources=[])
