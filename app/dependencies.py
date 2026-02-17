from fastapi import Depends
from app.services.eventHistory_service import EventHistoryService
from app.services.service_service import ServiceService
from app.services.schedule_service import ScheduleService
from app.repositories.eventHistory_repo import EventHistoryRepository
from app.repositories.service_repo import ServiceRepository
from app.repositories.schedule_repo import ScheduleRepository


# Repository providers
def get_event_history_repository() -> EventHistoryRepository:
    return EventHistoryRepository()


def get_service_repository() -> ServiceRepository:
    return ServiceRepository()


def get_schedule_repository() -> ScheduleRepository:
    return ScheduleRepository()


# Service providers with dependency injection
def get_event_history_service(
    repo: EventHistoryRepository = Depends(get_event_history_repository)
) -> EventHistoryService:
    return EventHistoryService(repo)


def get_service_service(
    repo: ServiceRepository = Depends(get_service_repository)
) -> ServiceService:
    return ServiceService(repo)


def get_schedule_service(
    schedule_repo: ScheduleRepository = Depends(get_schedule_repository),
    service_repo: ServiceRepository = Depends(get_service_repository),
    event_history_service: EventHistoryService = Depends(get_event_history_service)
) -> ScheduleService:
    return ScheduleService(schedule_repo, service_repo, event_history_service)

