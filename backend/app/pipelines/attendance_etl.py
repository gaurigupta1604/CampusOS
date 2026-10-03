from dataclasses import dataclass
import pandas as pd
REQUIRED={"student_id","course_id","session_date","present"}
@dataclass
class ValidationResult:valid:bool;errors:list[str];rows:int
def validate(frame:pd.DataFrame):
    errors=[];missing=REQUIRED-set(frame.columns)
    if missing:errors.append("Missing columns: "+", ".join(sorted(missing)))
    if not missing:
        if frame[["student_id","course_id","session_date"]].duplicated().any():errors.append("Duplicate student/course/session records detected")
        if not frame["present"].isin([True,False,0,1]).all():errors.append("present must be boolean")
    return ValidationResult(not errors,errors,len(frame))
def transform(frame:pd.DataFrame):
    check=validate(frame)
    if not check.valid:raise ValueError("; ".join(check.errors))
    clean=frame.copy();clean["session_date"]=pd.to_datetime(clean["session_date"],errors="raise").dt.date;clean["present"]=clean["present"].astype(bool)
    aggregates=clean.groupby(["student_id","course_id"],as_index=False).agg(classes_conducted=("present","size"),classes_attended=("present","sum"));aggregates["attendance_percentage"]=(aggregates.classes_attended/aggregates.classes_conducted*100).round(2)
    return clean,aggregates
