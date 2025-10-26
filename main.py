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
    results
