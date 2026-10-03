from datetime import date,datetime,timedelta
from app.core.database import Base,SessionLocal,engine
from app.core.security import hash_password
from app.models.domain import *
def seed():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        existing=db.query(User).filter_by(email="student@campusos.local").first()
        if existing:
            student=db.query(Student).filter_by(user_id=existing.id).first()
            if student and not db.query(Assignment).first():
                courses=db.query(Course).all()
                for index,course in enumerate(courses):
                    db.add(Assignment(course_id=course.id,title=f"{course.title} applied assignment",due_at=datetime.utcnow()+timedelta(days=index+2),max_marks=100))
                    db.add(Mark(student_id=student.id,course_id=course.id,assessment="Mid-semester",score=78+index*6,maximum=100))
                db.add(Complaint(reporter_id=existing.id,description="Hostel Wi-Fi disconnects during evening study hours",category="networking",location="Hostel A, Floor 2",priority=Priority.MEDIUM,status=ComplaintStatus.IN_PROGRESS))
                db.add_all([Notification(user_id=existing.id,title="Registration closes Friday",message="Complete mid-semester registration before 17:00 Friday.",priority=Priority.HIGH),Notification(user_id=existing.id,title="AI Builders Meetup",message="Applications are open for this week's meetup.",priority=Priority.MEDIUM)])
                db.commit()
            return
        cse=Department(code="CSE",name="Computer Science & Engineering");db.add(cse);db.flush()
        admin=User(email="admin@campusos.local",full_name="Campus Administrator",password_hash=hash_password("Admin123!"),role=Role.ADMIN);faculty_user=User(email="faculty@campusos.local",full_name="Dr. Maya Rao",password_hash=hash_password("Faculty123!"),role=Role.FACULTY);student_user=User(email="student@campusos.local",full_name="Gauri Gupta",password_hash=hash_password("Student123!"),role=Role.STUDENT);maintenance=User(email="maintenance@campusos.local",full_name="Facilities Team",password_hash=hash_password("Maintain123!"),role=Role.MAINTENANCE)
        db.add_all([admin,faculty_user,student_user,maintenance]);db.flush();db.add(Faculty(user_id=faculty_user.id,department_id=cse.id,designation="Assistant Professor"));student=Student(user_id=student_user.id,department_id=cse.id,registration_number="CSE2026001",semester=4,interests="artificial intelligence hackathons data science",skills="Python FastAPI SQL machine learning");db.add(student);db.flush()
        cn=Course(code="CS401",title="Computer Networks",department_id=cse.id);dbms=Course(code="CS402",title="Database Systems",department_id=cse.id);db.add_all([cn,dbms]);db.flush();db.add_all([Enrollment(student_id=student.id,course_id=cn.id,semester=4),Enrollment(student_id=student.id,course_id=dbms.id,semester=4)])
        for i in range(25):db.add(AttendanceRecord(student_id=student.id,course_id=cn.id,session_date=date.today()-timedelta(days=25-i),present=i not in {2,5,8,11,14,18,21}))
        for i in range(28):db.add(AttendanceRecord(student_id=student.id,course_id=dbms.id,session_date=date.today()-timedelta(days=28-i),present=i not in {4,12,20,26}))
        db.add_all([Event(title="AI Builders Meetup",description="Applied AI projects and peer demos",category="Artificial Intelligence",starts_at=datetime.utcnow()+timedelta(days=4),location="Innovation Hall",skills="Python machine learning"),Event(title="Open Source Sprint",description="Contribute to community software",category="Software Engineering",starts_at=datetime.utcnow()+timedelta(days=8),location="CSE Lab",skills="Git GitHub Python")]);db.commit()
if __name__=="__main__":seed()
