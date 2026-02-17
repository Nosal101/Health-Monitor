from fastapi import FastAPI
from threading import Event, Thread

from app.db import init_db
from app.routers import schedule_router, service_router, eventHistory_router
from app.tasks import run_auto_ping_loop

app = FastAPI()

stop_event = Event()
ping_thread: Thread | None = None

@app.on_event("startup")
def on_startup():
    global ping_thread
    init_db()
    ping_thread = Thread(target=run_auto_ping_loop, args=(stop_event,), daemon=True)
    ping_thread.start()


@app.on_event("shutdown")
def on_shutdown():
    stop_event.set()


app.include_router(service_router.router)
app.include_router(schedule_router.router)
app.include_router(eventHistory_router.router)
