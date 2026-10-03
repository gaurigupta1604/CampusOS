import json
from dataclasses import asdict,dataclass,field
from datetime import datetime,timezone
from app.core.config import settings
@dataclass(frozen=True)
class DomainEvent: name:str;aggregate_id:str;payload:dict;occurred_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
class EventPublisher:
    def publish(self,event:DomainEvent):
        try:
            from redis import Redis
            Redis.from_url(settings.redis_url).publish("campusos.events",json.dumps(asdict(event)))
        except Exception:return False
        return True
