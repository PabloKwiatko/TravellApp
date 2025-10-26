import requests
from fastapi import FastAPI
import os

app = FastAPI()

API_KEY = os.getenv("GOOGLE_API_KEY")  # Pobiera klucz z Railway Variables

@app.get("/")
def root():
    return {
        "status": "OK",
        "app": "Travell App",
        "message": "Witamy w Travell App! Twój backend działa poprawnie 🚀"
    }

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
    results = requests.get(url).json().get("results", [])
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
