from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import current_user
from app.core.database import get_db
from app.models.domain import Event,Student,User
from app.services.recommendations import recommend_events
router=APIRouter(prefix="/events",tags=["events"])
@router.get("/recommended")
def recommended(user:User=Depends(current_user),db:Session=Depends(get_db),limit:int=5):
    student=db.query(Student).filter_by(user_id=user.id).first()
    if not student:return[]
    events=db.scalars(select(Event).order_by(Event.starts_at).limit(100)).all()
    return recommend_events(student.interests,student.skills,events,min(max(limit,1),20))
