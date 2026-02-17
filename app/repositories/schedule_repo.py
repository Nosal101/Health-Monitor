from sqlmodel import Session, select
from app.models.schedule import Schedule
from app.db import engine

class ScheduleRepository:
    def create(self, schedule: Schedule) -> Schedule:
        with Session(engine) as session:
            session.add(schedule)
            session.commit()
            session.refresh(schedule)
            return schedule
        
    def update(self, schedule: Schedule) -> Schedule:
        with Session(engine) as session:
            session.add(schedule)
            session.commit()
            session.refresh(schedule)
            return schedule
        
    def get_by_service_id(self, service_id: int) -> Schedule | None:
        with Session(engine) as session:
            return session.exec(select(Schedule).where(Schedule.service_id == service_id)).first()

    def get_by_id(self, schedule_id: int) -> Schedule | None:
        with Session(engine) as session:
            return session.get(Schedule, schedule_id)

    def list_all(self) -> list[Schedule]:
        with Session(engine) as session:
            return session.exec(select(Schedule)).all()
