import requests
from fastapi import FastAPI
import os

API_KEY = os.getenv("AIzaSyBasrkaL6jidlX24iPdZaZ85Wv43uqM5ug")  # Pobiera klucz z Railway ENV Variable

app = FastAPI()

def search_google_places(country, category, location=None, radius=60000):
    if location:
        lat, lon = location
        loc_str = f"&location={lat},{lon}&radius={radius}"
    else:
        loc_str = ""
    url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json?"
        f"query={category}+in+{country}{loc_str}&key={API_KEY}"
    )
    results = requests.get(url).json()["results"]
    return [
        {
            "name": r["name"],
            "address": r.get("formatted_address", ""),
            "photo": r.get("photos", [{}])[0].get("photo_reference", ""),
            "location": r["geometry"]["location"],
            "rating": r.get("rating", None),
        }
        for r in results
    ]

@app.get("/travel-plan")
def get_travel_plan(country: str, transport: str = "Motocykl"):
    temples = search_google_places(country, "temple")
    viewpoints = search_google_places(country, "viewpoint")
    return {
        "temples": temples,
        "viewpoints": viewpoints,
    }
