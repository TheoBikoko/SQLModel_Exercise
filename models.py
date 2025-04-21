from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Relationship

class ArtistFestivalLink(SQLModel, table=True):
    artist_id: Optional[int] = Field(default=None, foreign_key="artist.id", primary_key=True)
    festival_id: Optional[int] = Field(default=None, foreign_key="festival.id", primary_key=True)

class ArtistBase(SQLModel):
    name: str = Field(index=True)
    real_name: str
    age: int
    genre: str

class Artist(ArtistBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    festivals: list["Festival"] = Relationship(back_populates="artists", link_model= ArtistFestivalLink)

class ArtistCreate(ArtistBase):
    pass

class ArtistPublic(ArtistBase):
    id: int

class ArtistUpdate(SQLModel):
    name: Optional[str] = None
    real_name: Optional[str] = None
    age: Optional[int] = None
    genre: Optional[str] = None

class FestivalBase(SQLModel):
    name: str  = Field(index=True)
    crowd_capacity: int
    start_date: date
    end_date: date
    location: str

class Festival(FestivalBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    artists: list[Artist] = Relationship(back_populates="festivals", link_model= ArtistFestivalLink)

class FestivalCreate(FestivalBase):
    pass

class FestivalPublic(FestivalBase):
    id: int

class FestivalUpdate(SQLModel):
    name: Optional[str] = None
    crowd_capacity: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: Optional[str] = None

