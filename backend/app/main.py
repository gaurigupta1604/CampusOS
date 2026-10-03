import time,uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI,Request,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST,Counter,Histogram,generate_latest
from app.api.routes import attendance,auth,campus,complaints,events,ml
from app.core.config import settings
from app.core.logging import logger
REQUESTS=Counter("campusos_http_requests_total","HTTP requests",["method","path","status"]);LATENCY=Histogram("campusos_http_latency_seconds","HTTP latency",["method","path"])
@asynccontextmanager
async def lifespan(app):logger.info("application.started",environment=settings.environment);yield;logger.info("application.stopped")
app=FastAPI(title=settings.app_name,version="0.1.0",lifespan=lifespan,docs_url="/api/docs",openapi_url="/api/openapi.json")
app.add_middleware(CORSMiddleware,allow_origins=settings.allowed_origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.middleware("http")
async def observe(request:Request,call_next):
    started=time.perf_counter();request_id=request.headers.get("x-request-id",str(uuid.uuid4()))
    try:response=await call_next(request)
    except Exception:logger.exception("http.unhandled",request_id=request_id,path=request.url.path);raise
    elapsed=time.perf_counter()-started;route=request.scope.get("route");path=getattr(route,"path",request.url.path);REQUESTS.labels(request.method,path,response.status_code).inc();LATENCY.labels(request.method,path).observe(elapsed);response.headers["x-request-id"]=request_id;logger.info("http.completed",request_id=request_id,method=request.method,path=path,status=response.status_code,latency_ms=round(elapsed*1000,2));return response
@app.get("/health")
def health():return{"status":"healthy","service":"api","version":"0.1.0"}
@app.get("/metrics",include_in_schema=False)
def metrics():return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)
for router in (auth.router,attendance.router,campus.router,complaints.router,events.router,ml.router):app.include_router(router,prefix="/api/v1")
connections:set[WebSocket]=set()
@app.websocket("/ws/notifications")
async def notifications(socket:WebSocket):
    await socket.accept();connections.add(socket)
    try:
        while True:await socket.receive_text()
    except WebSocketDisconnect:connections.discard(socket)
