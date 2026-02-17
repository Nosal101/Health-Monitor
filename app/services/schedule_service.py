from app.repositories.schedule_repo import ScheduleRepository
from app.repositories.service_repo import ServiceRepository
from app.services.eventHistory_service import EventHistoryService
from app.models.schedule import Schedule
import httpx
from datetime import datetime
import time


MIN_INTERVAL_SECONDS = 10
PING_TIMEOUT_SECONDS = 5.0

class ScheduleService:
    def __init__(
        self,
        schedule_repo: ScheduleRepository,
        service_repo: ServiceRepository,
        event_history_service: EventHistoryService
    ):
        self.schedule_repo = schedule_repo
        self.service_repo = service_repo
        self.event_history_service = event_history_service

    def _validate_interval(self, interval_seconds: int) -> None:
        if interval_seconds < MIN_INTERVAL_SECONDS:
            raise ValueError(f"Interval must be at least {MIN_INTERVAL_SECONDS} seconds")

    def _require_service_exists(self, service_id: int):
        service = self.service_repo.get_by_id(service_id)
        if not service:
            raise ValueError(f"Service {service_id} does not exist")
        return service

    def _mark_schedule_ran(self, schedule: Schedule) -> None:
        schedule.last_run = datetime.utcnow()
        self.schedule_repo.update(schedule)

    def create_schedule(self, service_id: int, interval_seconds: int) -> Schedule:
        self._validate_interval(interval_seconds)
        self._require_service_exists(service_id)

        if self.schedule_repo.get_by_service_id(service_id):
            raise ValueError(f"Service {service_id} already has a schedule")

        schedule = Schedule(service_id=service_id, interval_seconds=interval_seconds)
        return self.schedule_repo.create(schedule)
    
    def overwrite_schedule(self, service_id: int, interval_seconds: int) -> Schedule:
        self._validate_interval(interval_seconds)
        self._require_service_exists(service_id)

        existing = self.schedule_repo.get_by_service_id(service_id)
        if existing:
            existing.interval_seconds = interval_seconds
            return self.schedule_repo.update(existing)
        else:
            schedule = Schedule(service_id=service_id, interval_seconds=interval_seconds)
            return self.schedule_repo.create(schedule)
    
    def list_schedules(self):
        return self.schedule_repo.list_all()
    
    def get_by_id(self, schedule_id: int) -> Schedule | None:
        return self.schedule_repo.get_by_id(schedule_id)
    
    def ping_service(self, schedule: Schedule) -> dict:
        service = self._require_service_exists(schedule.service_id)
        started = time.perf_counter()

        try:
            response = httpx.get(service.url, timeout=5)
            latency = (time.perf_counter() - started) * 1000
        except httpx.RequestError as e:
            self._mark_schedule_ran(schedule)
            result = {
                "service_id": service.id,
                "status": "DOWN",
                "http_status": None,
                "latency_ms": None,
                "error_message": str(e)
            }
            self.event_history_service.record_ping_result(
                service_id=service.id,
                status="DOWN",
                error_message=str(e)
            )
            return result

        status = "UP" if response.status_code == service.expected_status else "DOWN"
        self._mark_schedule_ran(schedule)
        result = {
            "service_id": service.id,
            "status": status,
            "http_status": response.status_code,
            "latency_ms": latency,
            "error_message": None if status == "UP" else f"Expected {service.expected_status}"
        }
        self.event_history_service.record_ping_result(
            service_id=service.id,
            status=status,
            http_status=response.status_code,
            latency_ms=latency,
            error_message=result["error_message"]
        )
        return result
