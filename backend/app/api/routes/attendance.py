from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import allow,current_user
from app.core.database import get_db
from app.models.domain import AttendanceRecord,Role,Student,User
from app.schemas.domain import AttendanceCreate,AttendanceInsight
from app.services.attendance import AttendanceService
router=APIRouter(prefix="/attendance",tags=["attendance"])
@router.get("/students/{student_id}/courses/{course_id}/insight",response_model=AttendanceInsight)
def insight(student_id:int,course_id:int,user:User=Depends(current_user),db:Session=Depends(get_db)):
    if user.role==Role.STUDENT:
        student=db.query(Student).filter_by(user_id=user.id).first()
        if not student or student.id!=student_id:raise HTTPException(403,"You can only view your own attendance")
    elif user.role not in (Role.FACULTY,Role.ADMIN):raise HTTPException(403,"Insufficient permissions")
    return AttendanceService(db).insight(student_id,course_id)
@router.post("/records",status_code=201)
def record(payload:AttendanceCreate,user:User=Depends(allow(Role.FACULTY,Role.ADMIN)),db:Session=Depends(get_db)):
    row=db.query(AttendanceRecord).filter_by(student_id=payload.student_id,course_id=payload.course_id,session_date=payload.session_date).first()
    if row:row.present=payload.present;row.source=user.role.value
    else:row=AttendanceRecord(**payload.model_dump(),source=user.role.value);db.add(row)
    db.commit();return{"id":row.id,"status":"recorded"}
