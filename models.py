import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

class Artist(SQLModel, Table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    real_name: str
    age: int

class Festival(SQLModel, Table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    crowd_capacity: int
    start_date: datetime.date
    end_date: datetime.date