import requests
from fastapi import FastAPI, Query
import os

app = FastAPI()
API_KEY = os.getenv("GOOGLE_API_KEY")

WELCOME_MESSAGES = {
    "pl": "Witamy w Travell App! Twój backend działa poprawnie 🚀",
    "en": "Welcome to Travell App! Your backend is running smoothly 🚀",
    "no": "Velkommen til Travell App! Din backend kjører perfekt 🚀"
}

NO_RESULTS_MESSAGES = {
    "pl": "Brak wyników dla podanych parametrów.",
    "en": "No results for the specified parameters.",
    "no": "Ingen resultater for de oppgitte parametrene."
}

@app.get("/")
def root(lang: str = Query(default="pl", enum=["pl", "en", "no"])):
    return {
        "status": "OK",
        "app": "Travell App",
        "message": WELCOME_MESSAGES.get(lang, WELCOME_MESSAGES["pl"])
    }

@app.get("/test")
def test(lang: str = Query(default="pl", enum=["pl", "en", "no"])):
    messages = {
        "pl": "To jest testowy endpoint TravellApp",
        "en": "This is a test endpoint of TravellApp",
        "no": "Dette er test-endpointet til TravellApp"
    }
    return {"msg": messages.get(lang, messages["pl"])}

def translate_text(text, target_lang):
    translations = {
        "temple": {
            "pl": "świątynia",
            "en": "temple",
            "no": "tempel"
        },
        "viewpoint": {
            "pl": "punkt widokowy",
            "en": "viewpoint",
            "no": "utsiktspunkt"
        },
        "museum": {
            "pl": "muzeum",
            "en": "museum",
            "no": "museum"
        },
        "park": {
            "pl": "park",
            "en": "park",
            "no": "park"
        },
        "stadium": {
            "pl": "stadion",
            "en": "stadium",
            "no": "stadion"
        }
    }
    return translations.get(text.lower(), {}).get(target_lang, text)

def search_google_places(country, category, city=None, location=None, radius=60000, lang="pl"):
    city_part = f"+{city}" if city else ""
    query = f"{category}{city_part}+in+{country}"
    if location:
        lat, lon = location
        loc_str = f"&location={lat},{lon}&radius={radius}"
    else:
        loc_str = f"&radius={radius}"
    url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json?"
        f"query={query}{loc_str}&key={API_KEY}&language={lang}"
    )
    results = requests.get(url).json().get("results", [])
    return [
        {
            "name": r["name"],
            "translated_category": translate_text(category, lang),
            "address": r.get("formatted_address", ""),
            "photo": r.get("photos", [{}])[0].get("photo_reference", ""),
            "location": r["geometry"]["location"],
            "rating": r.get("rating", None),
        }
        for r in results
    ]

@app.get("/travel-plan")
def get_travel_plan(
    country: str,
    city: str = Query(default=None),
    category: str = Query(default="temple"),
    transport: str = Query(default="Motocykl"),
    radius: int = Query(default=60000),
    lang: str = Query(default="pl", enum=["pl", "en", "no"])
):
    places = search_google_places(country, category, city=city, radius=radius, lang=lang)
    if not places:
        return {
            "message": NO_RESULTS_MESSAGES.get(lang, NO_RESULTS_MESSAGES["pl"]),
            "country": country,
            "city": city,
            "category": category,
            "category_translated": translate_text(category, lang),
            "transport": transport,
            "radius": radius,
            "language": lang,
            "places": []
        }
    else:
        return {
            "country": country,
            "city": city,
            "category": category,
            "category_translated": translate_text(category, lang),
            "transport": transport,
            "radius": radius,
            "language": lang,
            "places": places
        }
