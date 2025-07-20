import spacy
from geopy.geocoders import Nominatim
from app.config import SPACY_MODEL
import sqlite3
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nlp = spacy.load(SPACY_MODEL)
geolocator = Nominatim(user_agent="osint_dashboard")

def init_cache(db_path="osint.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            name TEXT PRIMARY KEY,
            latitude TEXT,
            longitude TEXT
        )
    """)
    conn.commit()
    return conn, cursor

def cache_location(cursor, conn, name):
    cursor.execute("SELECT latitude, longitude FROM locations WHERE name = ?", (name,))
    result = cursor.fetchone()
    if result:
        return {'name': name, 'latitude': result[0], 'longitude': result[1]}
    try:
        location = geolocator.geocode(name, timeout=10)
        if location:
            cursor.execute("INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)",
                           (name, str(location.latitude), str(location.longitude)))
            conn.commit()
            return {'name': name, 'latitude': str(location.latitude), 'longitude': str(location.longitude)}
    except Exception as e:
        logger.error(f"Error geocoding {name}: {e}")
    return None

def extract_locations(text: str) -> List[Dict[str, str]]:
    conn, cursor = init_cache()
    doc = nlp(text)
    locations = []
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC']:
            location = cache_location(cursor, conn, ent.text)
            if location:
                locations.append(location)
    conn.close()
    return locations
