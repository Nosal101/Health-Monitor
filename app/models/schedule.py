from sqlmodel import SQLModel, Field
from datetime import datetime

class Schedule(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    service_id: int
    interval_seconds: int
    active: bool = Field(default=True)
    last_run: datetime | None = None 
