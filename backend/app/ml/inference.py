from app.schemas.domain import RiskInput
MODEL_VERSION="rule-baseline-1.0"
def predict_attendance_risk(data:RiskInput):
    factors=[];score=0.0
    if data.current_attendance<75:score+=.42;factors.append("attendance below threshold")
    if data.attendance_trend<0:score+=min(.25,abs(data.attendance_trend)/100);factors.append("declining trend")
    if data.recent_absence_frequency>.3:score+=.22;factors.append("frequent recent absences")
    if data.historical_attendance<75:score+=.16;factors.append("historical attendance below threshold")
    probability=min(.99,max(.01,score));level="high" if probability>=.7 else "medium" if probability>=.4 else "low"
    return {"risk_level":level,"probability":round(probability,3),"contributing_factors":factors or ["no material risk factors detected"],"model_version":MODEL_VERSION}
