import math
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.domain import AttendanceRecord
class AttendanceService:
    threshold=75.0
    def __init__(self,db:Session):self.db=db
    def insight(self,student_id:int,course_id:int):
        rows=list(self.db.scalars(select(AttendanceRecord).where(AttendanceRecord.student_id==student_id,AttendanceRecord.course_id==course_id).order_by(AttendanceRecord.session_date)))
        total=len(rows);attended=sum(r.present for r in rows);current=round(attended/total*100,2) if total else 0
        needed=0 if current>=self.threshold else math.ceil((self.threshold*total-100*attended)/(100-self.threshold))
        can_miss=max(0,math.floor(attended/(self.threshold/100)-total)) if total else 0
        recent=rows[-5:];recent_rate=sum(r.present for r in recent)/len(recent)*100 if recent else current;trend=round(recent_rate-current,2)
        projected=round((attended+sum(r.present for r in recent))/(total+len(recent))*100,2) if recent else current
        probability=min(.99,max(.01,(self.threshold-current)/30+.5-trend/100));risk="high" if probability>=.7 else "medium" if probability>=.4 else "low"
        factors=[]
        if current<self.threshold:factors.append("Current attendance is below the 75% threshold")
        if trend<0:factors.append("Recent attendance trend is declining")
        if total<5:factors.append("Limited history increases uncertainty")
        return {"current_attendance":current,"threshold":self.threshold,"classes_conducted":total,"classes_attended":attended,"classes_needed":needed,"classes_can_miss":can_miss,"projected_attendance":projected,"trend":trend,"risk_level":risk,"probability":round(probability,3),"contributing_factors":factors or ["Attendance is stable above the threshold"]}
