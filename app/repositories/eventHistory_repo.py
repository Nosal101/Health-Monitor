from sqlmodel import Session, select
from app.models.eventHistory import EventHistory
from app.db import engine

class EventHistoryRepository:
    def create(self, event_history: EventHistory) -> EventHistory:
        with Session(engine) as session:
            session.add(event_history)
            session.commit()
            session.refresh(event_history)
            return event_history

    def list_all(self) -> list[EventHistory]:
        with Session(engine) as session:
            return session.exec(select(EventHistory)).all()
        
    def list_by_service_id(self, service_id: int) -> list[EventHistory]:
        with Session(engine) as session:
            return session.exec(select(EventHistory).where(EventHistory.service_id == service_id)).all()
    