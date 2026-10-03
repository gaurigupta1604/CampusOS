import re
from sqlalchemy.orm import Session
from app.models.domain import AuditLog,Complaint,Priority
RULES={"electrical":["power","light","socket","wire","electric"],"plumbing":["leak","tap","water","pipe","toilet"],"networking":["wifi","internet","network","router"],"cleanliness":["dirty","waste","garbage","clean"],"security":["unsafe","theft","security","harassment"],"hvac":["ac","air conditioning","ventilation"],"furniture":["chair","desk","table","furniture"]}
class ComplaintService:
    def __init__(self,db:Session):self.db=db
    def classify(self,text):
        low=text.lower();scores={k:sum(word in low for word in words) for k,words in RULES.items()};category=max(scores,key=scores.get) if max(scores.values(),default=0)>0 else "infrastructure"
        critical=any(x in low for x in ("fire","sparking","gas leak","danger","injury"));urgent=any(x in low for x in ("flood","no power","unsafe","broken lock"));priority=Priority.CRITICAL if critical else Priority.HIGH if urgent else Priority.MEDIUM
        return category,priority
    def create(self,user_id,description,location,category=None):
        predicted,priority=self.classify(description);item=Complaint(reporter_id=user_id,description=description,location=location,category=category or predicted,priority=priority);self.db.add(item);self.db.flush();self.db.add(AuditLog(actor_id=user_id,action="complaint.created",entity_type="complaint",entity_id=str(item.id),detail=f"category={item.category};priority={priority.value}"));self.db.commit();self.db.refresh(item);return item
