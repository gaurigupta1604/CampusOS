import enum
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Role(str,enum.Enum): STUDENT="student"; FACULTY="faculty"; ADMIN="admin"; CLUB_COORDINATOR="club_coordinator"; MAINTENANCE="maintenance"
class ComplaintStatus(str,enum.Enum): OPEN="open"; ASSIGNED="assigned"; IN_PROGRESS="in_progress"; RESOLVED="resolved"; CLOSED="closed"
class Priority(str,enum.Enum): LOW="low"; MEDIUM="medium"; HIGH="high"; CRITICAL="critical"
class User(Base):
    __tablename__="users"; id:Mapped[int]=mapped_column(primary_key=True); email:Mapped[str]=mapped_column(String(255),unique=True,index=True); full_name:Mapped[str]=mapped_column(String(150)); password_hash:Mapped[str]=mapped_column(String(255)); role:Mapped[Role]=mapped_column(Enum(Role),index=True); is_active:Mapped[bool]=mapped_column(Boolean,default=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Department(Base):
    __tablename__="departments"; id:Mapped[int]=mapped_column(primary_key=True); code:Mapped[str]=mapped_column(String(20),unique=True); name:Mapped[str]=mapped_column(String(150),unique=True)
class Student(Base):
    __tablename__="students"; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),unique=True); department_id:Mapped[int]=mapped_column(ForeignKey("departments.id"),index=True); registration_number:Mapped[str]=mapped_column(String(40),unique=True); semester:Mapped[int]; interests:Mapped[str]=mapped_column(Text,default=""); skills:Mapped[str]=mapped_column(Text,default=""); user=relationship("User"); department=relationship("Department")
class Faculty(Base):
    __tablename__="faculty"; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),unique=True); department_id:Mapped[int]=mapped_column(ForeignKey("departments.id"),index=True); designation:Mapped[str]=mapped_column(String(100)); user=relationship("User")
class Course(Base):
    __tablename__="courses"; id:Mapped[int]=mapped_column(primary_key=True); code:Mapped[str]=mapped_column(String(20),unique=True); title:Mapped[str]=mapped_column(String(150)); department_id:Mapped[int]=mapped_column(ForeignKey("departments.id"),index=True); credits:Mapped[int]=mapped_column(default=3)
class Enrollment(Base):
    __tablename__="enrollments"; __table_args__=(UniqueConstraint("student_id","course_id"),); id:Mapped[int]=mapped_column(primary_key=True); student_id:Mapped[int]=mapped_column(ForeignKey("students.id"),index=True); course_id:Mapped[int]=mapped_column(ForeignKey("courses.id"),index=True); semester:Mapped[int]; student=relationship("Student"); course=relationship("Course")
class AttendanceRecord(Base):
    __tablename__="attendance_records"; __table_args__=(UniqueConstraint("student_id","course_id","session_date"),); id:Mapped[int]=mapped_column(primary_key=True); student_id:Mapped[int]=mapped_column(ForeignKey("students.id"),index=True); course_id:Mapped[int]=mapped_column(ForeignKey("courses.id"),index=True); session_date:Mapped[date]=mapped_column(Date,index=True); present:Mapped[bool]; source:Mapped[str]=mapped_column(String(30),default="faculty"); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Assignment(Base):
    __tablename__="assignments"; id:Mapped[int]=mapped_column(primary_key=True); course_id:Mapped[int]=mapped_column(ForeignKey("courses.id"),index=True); title:Mapped[str]=mapped_column(String(180)); due_at:Mapped[datetime]; max_marks:Mapped[float]=mapped_column(Float,default=100)
class Mark(Base):
    __tablename__="marks"; id:Mapped[int]=mapped_column(primary_key=True); student_id:Mapped[int]=mapped_column(ForeignKey("students.id"),index=True); course_id:Mapped[int]=mapped_column(ForeignKey("courses.id"),index=True); assessment:Mapped[str]=mapped_column(String(100)); score:Mapped[float]; maximum:Mapped[float]
class Event(Base):
    __tablename__="events"; id:Mapped[int]=mapped_column(primary_key=True); title:Mapped[str]=mapped_column(String(180)); description:Mapped[str]=mapped_column(Text); category:Mapped[str]=mapped_column(String(80),index=True); starts_at:Mapped[datetime]=mapped_column(index=True); location:Mapped[str]=mapped_column(String(180)); skills:Mapped[str]=mapped_column(Text,default=""); capacity:Mapped[int]=mapped_column(default=100)
class Club(Base):
    __tablename__="clubs"; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(150),unique=True); category:Mapped[str]=mapped_column(String(80)); description:Mapped[str]=mapped_column(Text)
class Complaint(Base):
    __tablename__="complaints"; id:Mapped[int]=mapped_column(primary_key=True); reporter_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True); assignee_id:Mapped[int|None]=mapped_column(ForeignKey("users.id"),nullable=True,index=True); description:Mapped[str]=mapped_column(Text); category:Mapped[str]=mapped_column(String(50),index=True); location:Mapped[str]=mapped_column(String(180)); priority:Mapped[Priority]=mapped_column(Enum(Priority),index=True); status:Mapped[ComplaintStatus]=mapped_column(Enum(ComplaintStatus),default=ComplaintStatus.OPEN,index=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True); resolved_at:Mapped[datetime|None]=mapped_column(nullable=True)
class Notification(Base):
    __tablename__="notifications"; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True); title:Mapped[str]=mapped_column(String(180)); message:Mapped[str]=mapped_column(Text); priority:Mapped[Priority]=mapped_column(Enum(Priority),default=Priority.MEDIUM); is_read:Mapped[bool]=mapped_column(Boolean,default=False,index=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True)
class AuditLog(Base):
    __tablename__="audit_logs"; id:Mapped[int]=mapped_column(primary_key=True); actor_id:Mapped[int|None]=mapped_column(ForeignKey("users.id"),nullable=True,index=True); action:Mapped[str]=mapped_column(String(100),index=True); entity_type:Mapped[str]=mapped_column(String(80)); entity_id:Mapped[str]=mapped_column(String(80)); detail:Mapped[str]=mapped_column(Text,default=""); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True)
class ModelPrediction(Base):
    __tablename__="model_predictions"; id:Mapped[int]=mapped_column(primary_key=True); student_id:Mapped[int]=mapped_column(ForeignKey("students.id"),index=True); model_name:Mapped[str]=mapped_column(String(100),index=True); model_version:Mapped[str]=mapped_column(String(40)); risk_level:Mapped[str]=mapped_column(String(30)); probability:Mapped[float]; explanation:Mapped[str]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True)
