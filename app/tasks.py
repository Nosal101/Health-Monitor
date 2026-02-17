from datetime import datetime
from threading import Event
import time

from app.services.schedule_service import ScheduleService
from app.services.eventHistory_service import EventHistoryService
from app.repositories.schedule_repo import ScheduleRepository
from app.repositories.service_repo import ServiceRepository
from app.repositories.eventHistory_repo import EventHistoryRepository


AUTO_PING_POLL_SECONDS = 5


def _is_schedule_due(last_run: datetime | None, interval_seconds: int) -> bool:
	if last_run is None:
		return True
	elapsed_seconds = (datetime.utcnow() - last_run).total_seconds()
	return elapsed_seconds >= interval_seconds


def run_due_pings_once() -> int:
	# Create dependencies manually for background task
	schedule_repo = ScheduleRepository()
	service_repo = ServiceRepository()
	event_history_repo = EventHistoryRepository()
	event_history_service = EventHistoryService(event_history_repo)
	schedule_service = ScheduleService(schedule_repo, service_repo, event_history_service)
	
	schedules = schedule_service.list_schedules()
	pinged_count = 0

	for schedule in schedules:
		if not schedule.active:
			continue
		if not _is_schedule_due(schedule.last_run, schedule.interval_seconds):
			continue

		try:
			schedule_service.ping_service(schedule)
			pinged_count += 1
		except ValueError:
			continue

	return pinged_count


def run_auto_ping_loop(stop_event: Event, poll_seconds: int = AUTO_PING_POLL_SECONDS) -> None:
	while not stop_event.is_set():
		run_due_pings_once()
		stop_event.wait(poll_seconds)

