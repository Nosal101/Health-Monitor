from fastapi import APIRouter, Depends, HTTPException
from app.services.schedule_service import ScheduleService
from app.dependencies import get_schedule_service
from app.schemas import ScheduleCreate, ScheduleResponse

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.post("/", response_model=ScheduleResponse, status_code=201)
def create_schedule(
    req: ScheduleCreate,
    service: ScheduleService = Depends(get_schedule_service)
):
    try:
        return service.create_schedule(req.service_id, req.interval_seconds)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/", response_model=ScheduleResponse)
def overwrite_schedule(
    req: ScheduleCreate,
    service: ScheduleService = Depends(get_schedule_service)
):
    try:
        return service.overwrite_schedule(req.service_id, req.interval_seconds)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ScheduleResponse])
def list_schedules(
    service: ScheduleService = Depends(get_schedule_service)
):
    return service.list_schedules()


@router.get("/ping/{schedule_id}")
def ping_schedule(
    schedule_id: int,
    service: ScheduleService = Depends(get_schedule_service)
):
    schedule = service.get_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return service.ping_service(schedule)
