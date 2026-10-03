from fastapi import APIRouter,Depends
from app.api.dependencies import allow
from app.models.domain import Role,User
from app.schemas.domain import RiskInput,RiskOutput
from app.ml.inference import predict_attendance_risk
router=APIRouter(prefix="/ml",tags=["machine-learning"])
@router.post("/attendance-risk",response_model=RiskOutput)
def attendance_risk(payload:RiskInput,user:User=Depends(allow(Role.FACULTY,Role.ADMIN))):return predict_attendance_risk(payload)
