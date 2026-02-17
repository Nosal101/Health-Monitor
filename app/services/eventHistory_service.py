from app.repositories.eventHistory_repo import EventHistoryRepository
from app.models.eventHistory import EventHistory
from datetime import datetime


class EventHistoryService:
    def __init__(self, repo: EventHistoryRepository):
        self.repo = repo

    def record_ping_result(
        self,
        service_id: int,
        status: str,
        http_status: int | None = None,
        latency_ms: float | None = None,
        error_message: str | None = None,
    ) -> EventHistory:
        """Record a ping result to event history."""
        event = EventHistory(
            service_id=service_id,
            timestamp=datetime.utcnow(),
            status=status,
            http_status=http_status,
            latency_ms=latency_ms,
            error_message=error_message,
        )
        return self.repo.create(event)

    def list_events_by_service(self, service_id: int) -> list[EventHistory]:
        return self.repo.list_by_service_id(service_id)

    def list_all_events(self) -> list[EventHistory]:
        return self.repo.list_all()
