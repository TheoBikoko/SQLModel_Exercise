import datetime
import requests

artists_url = "http://127.0.0.1:8000/artists"
festivals_url = "http://127.0.0.1:8000/festivals"

def read_artists():
    data = requests.get(f"{artists_url}")
    print(data.status_code)
    print(data.json())

def read_artist(artist_id: int):
    data = requests.get(f"{artists_url}/{artist_id}")
    print(data.status_code)
    print(data.json())

def create_artist():
    artist = {"name": "2Pac",
              "real_name": "Tupac Amaru Shakur",
              "age": 25}
    data = requests.post(f"{artists_url}", json=artist)
    print(data.status_code)
    print(data.json())

def update_artist(artist_id: int, new_data: dict):
    data = requests.patch(f"{artists_url}/{artist_id}", json=new_data)
    print(data)
    print(data.status_code)
    print(data.json())

def delete_artist(artist_id: int):
    data = requests.delete(f"{artists_url}/{artist_id}")
    print(data.status_code)
    print(data.json())

def read_festivals():
    data = requests.get(f"{festivals_url}")
    print(data.status_code)
    print(data.json())

def read_festival(festival_id: int):
    data = requests.get(f"{festivals_url}/{festival_id}")
    print(data.status_code)
    print(data.json())

def create_festival():
    festival = {"name": "Coachella",
                "crowd_capacity": 20000,
                "start_date": datetime.date(2025,6,19).isoformat(),
                "end_date": datetime.date(2025,6,25).isoformat()}
    data = requests.post(f"{festivals_url}", json=festival)
    print(data.status_code)
    print(data.json())

def update_festival(festival_id: int, new_data: dict):
    data = requests.patch(f"{festivals_url}/{festival_id}", json=new_data)
    print(data)
    print(data.status_code)
    print(data.json())

def delete_festival(festival_id: int):
    data = requests.delete(f"{festivals_url}/{festival_id}")
    print(data.status_code)
    print(data.json())

def get_festivals_from_artist_id(artist_id: int):
    data = requests.get(f"{artists_url}/festivals/{artist_id}")
    print(data.status_code)
    print(data.json())

def get_artists_from_festival_id(festival_id: int):
    data = requests.get(f"{festivals_url}/artists/{festival_id}")
    print(data.status_code)
    print(data.json())

def get_festivals_ordered_by_date(order: str):
    data = requests.get(f"{festivals_url}/date/{order}")
    print(data.status_code)
    print(data.json())

def get_festivals_based_on_location(festival_location: str):
    data = requests.get(f"{festivals_url}/location/{festival_location}")
    print(data.status_code)
    print(data.json())

def get_artists_based_on_genre(genre_name: str):
    data = requests.get(f"{artists_url}/genre/{genre_name}")
    print(data.status_code)
    print(data.json())

if __name__ == "__main__":
    read_artists()
    read_festivals()
    read_artist(1)
    read_festival(1)
    create_artist()
    create_festival()
    update_artist(1,{"name": "Lenny Kravitz", "real_name": "Leonard Albert Kravitz", "age": 60})
    update_festival(1,{"name": "VinyaRock", "crowd_capacity": 1500, "start_date": datetime.date(2025,7,19).isoformat(), "end_date": datetime.date(2025,8,25).isoformat()})
    delete_artist(15)
    delete_festival(15)
    get_festivals_from_artist_id(2)
    get_artists_from_festival_id(3)
    get_festivals_ordered_by_date("ascendent")
    get_festivals_ordered_by_date("descendent")
    get_festivals_based_on_location("USA")
    get_festivals_based_on_location("New York")
    get_festivals_based_on_location("Brooklyn")
    get_artists_based_on_genre("Hip-Hop")
    get_artists_based_on_genre("Pop")

