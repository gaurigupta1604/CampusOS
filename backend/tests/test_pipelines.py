import pandas as pd
from app.pipelines.attendance_etl import transform,validate
from app.schemas.domain import RiskInput
from app.ml.inference import predict_attendance_risk
def test_attendance_etl_calculates_real_aggregate():
    frame=pd.DataFrame([{"student_id":1,"course_id":2,"session_date":"2026-01-01","present":True},{"student_id":1,"course_id":2,"session_date":"2026-01-02","present":False}]);_,result=transform(frame);assert result.iloc[0].attendance_percentage==50
def test_duplicate_attendance_fails_validation():
    row={"student_id":1,"course_id":2,"session_date":"2026-01-01","present":True};assert not validate(pd.DataFrame([row,row])).valid
def test_risk_explanation_is_grounded():
    result=predict_attendance_risk(RiskInput(current_attendance=62,attendance_trend=-8,classes_conducted=20,classes_attended=12,historical_attendance=70,recent_absence_frequency=.5));assert result["risk_level"]=="high" and result["contributing_factors"]
