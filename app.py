from typing import List
from fastapi import FastAPI, HTTPException, Query, Depends
from sqlmodel import Session, select
from models import *
from database import engine, lifespan
from sqlalchemy import desc

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def welcome():
    welcome_message = ("""Welcome to the Artist & Festival API. This API allows you to create, read, update and delete both artists and festivals. Furthermore, there are additional features such as:
                       - View all the artists that will perform in a specific festival." 
                       - View all the festivals in which an artist will perform."
                       - View a list of all the festivals ordered by date (ascendent or descendent)."
                       - View festivals based on location, you can input the name of the country, state (for the USA) or city."
                       - View artists based on genre.""")
    return welcome_message

@app.get("/artists/", response_model=List[ArtistPublic])
def read_artists():
    with Session(engine) as session:
        artists = session.exec(select(Artist)).all()
        return artists

@app.get("/festivals/", response_model=List[FestivalPublic])
def read_festivals():
    with Session(engine) as session:
        festivals = session.exec(select(Festival)).all()
        return festivals

@app.get("/artists/{artist_id}", response_model=ArtistPublic)
def read_artist(artist_id: int):
    with Session(engine) as session:
        artist = session.get(Artist, artist_id)
        if not artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        return artist

@app.get("/festivals/{festival_id}", response_model=FestivalPublic)
def read_festival(festival_id: int):
    with Session(engine) as session:
        festival = session.get(Festival, festival_id)
        if not festival:
            raise HTTPException(status_code=404, detail="Festival not found")
        return festival

@app.post("/artists/", response_model=ArtistPublic)
def create_artist(artist: ArtistCreate):
    with Session(engine) as session:
        db_artist = Artist.model_validate(artist)
        session.add(db_artist)
        session.commit()
        session.refresh(db_artist)
        return db_artist

@app.post("/festivals/", response_model=FestivalPublic)
def create_festival(festival: FestivalCreate):
    with Session(engine) as session:
        db_festival = Festival.model_validate(festival)
        session.add(db_festival)
        session.commit()
        session.refresh(db_festival)
        return db_festival

@app.patch("/artists/{artist_id}", response_model=ArtistPublic)
def update_artist(artist_id: int, artist: ArtistUpdate):
    with Session(engine) as session:
        db_artist = session.get(Artist, artist_id)
        if not db_artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        artist_data = artist.model_dump(exclude_unset=True)
        for key, value in artist_data.items():
            setattr(db_artist, key, value)
        session.add(db_artist)
        session.commit()
        session.refresh(db_artist)
        return db_artist

@app.patch("/festivals/{festival_id}", response_model=FestivalPublic)
def update_festival(festival_id: int, festival: FestivalUpdate):
    with Session(engine) as session:
        db_festival = session.get(Festival, festival_id)
        if not db_festival:
            raise HTTPException(status_code=404, detail="Festival not found")
        festival_data = festival.model_dump(exclude_unset=True)
        for key, value in festival_data.items():
            setattr(db_festival, key, value)
        session.add(db_festival)
        session.commit()
        session.refresh(db_festival)
        return db_festival

@app.delete("/artists/{artist_id}")
def delete_artist(artist_id: int):
    with Session(engine) as session:
        artist = session.get(Artist, artist_id)
        if not artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        session.delete(artist)
        session.commit()
        return {"ok": True}

@app.delete("/festivals/{festival_id}")
def delete_festival(festival_id: int):
    with Session(engine) as session:
        festival = session.get(Festival, festival_id)
        if not festival:
            raise HTTPException(status_code=404, detail="Festival not found")
        session.delete(festival)
        session.commit()
        return {"ok": True}

@app.get("/artists/festivals/{artist_id}", response_model=list[FestivalPublic])
def get_festivals_from_artist_id(artist_id: int):
    with Session(engine) as session:
        artist = session.get(Artist, artist_id)
        if not artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        return artist.festivals

@app.get("/festivals/artists/{festival_id}", response_model=list[ArtistPublic])
def get_artists_from_festival_id(festival_id: int):
    with Session(engine) as session:
        festival = session.get(Festival, festival_id)
        if not festival:
            raise HTTPException(status_code=404, detail="Artists not found")
        return festival.artists

@app.get("/festivals/date/{order}", response_model=list[FestivalPublic])
def get_festivals_ordered_by_date(order: str):
    with Session(engine) as session:
        query = select(Festival)

        if order == "ascendent":
            query = query.order_by(Festival.start_date)
        elif order == "descendent":
            query = query.order_by(desc(Festival.start_date))
        else: raise HTTPException(status_code=400, detail="Invalid parameter, please write ascendent or descendent.")

        festivals_ordered = session.exec(query).all()

        if not festivals_ordered:
            raise HTTPException(status_code=404, detail="Festivals not found")
        return festivals_ordered

@app.get("/festivals/location/{festival_location}", response_model=list[FestivalPublic])
def get_festivals_based_on_location(festival_location: str):
    with Session(engine) as session:
        query = select(Festival).where(Festival.location.like(f"%{festival_location}%"))

        festivals_filtered = session.exec(query).all()

        if not festivals_filtered:
            raise HTTPException(status_code=404, detail="Festivals not found")
        return festivals_filtered

@app.get("/artists/genre/{genre_name}", response_model=list[ArtistPublic])
def get_artists_based_on_genre(genre_name: str):
    with Session(engine) as session:
        query = select(Artist).where(Artist.genre.like(f"%{genre_name}%"))

        artists_filtered = session.exec(query).all()

        if not artists_filtered:
            raise HTTPException(status_code=404, detail="Festivals not found")
        return artists_filtered


