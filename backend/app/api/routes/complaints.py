from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import current_user
from app.core.database import get_db
from app.models.domain import Complaint,Role,User
from app.schemas.domain import ComplaintCreate,ComplaintView
from app.services.complaints import ComplaintService
router=APIRouter(prefix="/complaints",tags=["complaints"])
@router.post("",response_model=ComplaintView,status_code=201)
def create(payload:ComplaintCreate,user:User=Depends(current_user),db:Session=Depends(get_db)):
    item=ComplaintService(db).create(user.id,payload.description,payload.location,payload.category)
    return ComplaintView(id=item.id,description=item.description,category=item.category,location=item.location,priority=item.priority.value,status=item.status.value,created_at=item.created_at)
@router.get("")
def list_complaints(user:User=Depends(current_user),db:Session=Depends(get_db),offset:int=0,limit:int=50,status:str|None=None):
    query=select(Complaint)
    if user.role==Role.STUDENT:query=query.where(Complaint.reporter_id==user.id)
    elif user.role==Role.MAINTENANCE:query=query.where(Complaint.assignee_id==user.id)
    if status:query=query.where(Complaint.status==status)
    rows=db.scalars(query.order_by(Complaint.created_at.desc()).offset(max(offset,0)).limit(min(max(limit,1),100))).all()
    return [{"id":x.id,"description":x.description,"category":x.category,"location":x.location,"priority":x.priority.value,"status":x.status.value,"created_at":x.created_at} for x in rows]
