from sqlmodel import SQLModel, Field

class Service(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    url: str
    expected_status: int = 200
