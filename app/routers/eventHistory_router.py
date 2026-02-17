from fastapi import APIRouter, Depends
from app.services.eventHistory_service import EventHistoryService
from app.dependencies import get_event_history_service


router = APIRouter(prefix="/event-history", tags=["event-history"])


@router.get("/")
def list_event_history(
    service: EventHistoryService = Depends(get_event_history_service)
):
    return service.list_all_events()


@router.get("/{service_id}")
def list_event_history_by_service_id(
    service_id: int,
    service: EventHistoryService = Depends(get_event_history_service)
):
    return service.list_events_by_service(service_id)
