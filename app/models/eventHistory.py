from sqlmodel import SQLModel, Field
from datetime import datetime

class EventHistory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    service_id: int = Field(index=True)
    timestamp: datetime | None = None  
    status: str  # "UP" or "DOWN"
    http_status: int | None = None
    latency_ms: float | None = None
    error_message: str | None = None
