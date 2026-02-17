from pydantic import BaseModel, Field
from datetime import datetime


# Service schemas
class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1)
    expected_status: int = Field(200, ge=100, le=599)


class ServiceResponse(BaseModel):
    id: int
    name: str
    url: str
    expected_status: int

    class Config:
        from_attributes = True


# Schedule schemas
class ScheduleCreate(BaseModel):
    service_id: int = Field(..., gt=0)
    interval_seconds: int = Field(..., ge=10, le=86400)


class ScheduleResponse(BaseModel):
    id: int
    service_id: int
    interval_seconds: int
    active: bool
    last_run: datetime | None

    class Config:
        from_attributes = True


# Event schemas
class EventResponse(BaseModel):
    id: int
    service_id: int
    timestamp: datetime
    status: str
    http_status: int | None
    latency_ms: float | None
    error_message: str | None

    class Config:
        from_attributes = True
