from typing import Optional
from pydantic import BaseModel


class SessionCreate(BaseModel):
    date: str
    type: str
    duration: int
    notes: str


class SessionUpdate(BaseModel):
    date: Optional[str] = None
    type: Optional[str] = None
    duration: Optional[int] = None
    notes: Optional[str] = None


class Session(BaseModel):
    id: int
    date: str
    type: str
    duration: int
    notes: str

    class Config:
        from_attributes = True