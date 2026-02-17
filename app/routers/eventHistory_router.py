from fastapi import APIRouter, Depends
from app.services.eventHistory_service import EventHistoryService
from app.dependencies import get_event_history_service
from app.schemas import EventResponse


router = APIRouter(prefix="/event-history", tags=["event-history"])


@router.get("/", response_model=list[EventResponse])
def list_event_history(
    service: EventHistoryService = Depends(get_event_history_service)
):
    return service.list_all_events()


@router.get("/{service_id}", response_model=list[EventResponse])
def list_event_history_by_service_id(
    service_id: int,
    service: EventHistoryService = Depends(get_event_history_service)
):
    return service.list_events_by_service(service_id)
