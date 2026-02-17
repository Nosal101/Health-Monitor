from sqlmodel import Session, select
from app.models.service import Service
from app.db import engine

class ServiceRepository:
    def create(self, service: Service) -> Service:
        with Session(engine) as session:
            session.add(service)
            session.commit()
            session.refresh(service)
            return service

    def get_all(self) -> list[Service]:
        with Session(engine) as session:
            return session.exec(select(Service)).all()

    def get_by_id(self, service_id: int) -> Service | None:
        with Session(engine) as session:
            return session.get(Service, service_id)

    def get_by_url(self, url: str) -> Service | None:
        with Session(engine) as session:
            return session.exec(select(Service).where(Service.url == url)).first()

    def delete(self, service_id: int) -> bool:
        with Session(engine) as session:
            service = session.get(Service, service_id)
            if not service:
                return False
            session.delete(service)
            session.commit()
            return True
