from pydantic import BaseModel, Field
from datetime import datetime


class Ticket(BaseModel):
    description: str
    date: datetime = Field(default_factory=datetime.now)
    status: str