from datetime import date, datetime
from pydantic import BaseModel, Field
class AttendanceCreate(BaseModel): student_id:int; course_id:int; session_date:date; present:bool
class AttendanceInsight(BaseModel): current_attendance:float; threshold:float; classes_conducted:int; classes_attended:int; classes_needed:int; classes_can_miss:int; projected_attendance:float; trend:float; risk_level:str; probability:float; contributing_factors:list[str]
class ComplaintCreate(BaseModel): description:str=Field(min_length=15,max_length=4000); location:str=Field(min_length=2,max_length=180); category:str|None=None
class ComplaintView(BaseModel): id:int; description:str; category:str; location:str; priority:str; status:str; created_at:datetime
class RiskInput(BaseModel): current_attendance:float=Field(ge=0,le=100); attendance_trend:float=Field(ge=-100,le=100); classes_conducted:int=Field(ge=0); classes_attended:int=Field(ge=0); historical_attendance:float=Field(ge=0,le=100); recent_absence_frequency:float=Field(ge=0,le=1)
class RiskOutput(BaseModel): risk_level:str; probability:float; contributing_factors:list[str]; model_version:str
class AssistantRequest(BaseModel): message:str=Field(min_length=1,max_length=1000)
class AssistantResponse(BaseModel): answer:str; tool:str; sources:list[str]=[]
