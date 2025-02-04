# Query: 
# ContextLines: 1

import time
import logging
import httpx
from fastapi import FastAPI, Query
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()
BASE_URL = "https://api.spaceflightnewsapi.net/v4"
RATE_LIMIT = 5  # Tiempo de espera entre peticiones para evitar bloqueos (segundos)

# Base de datos en memoria para deduplicación
db_articles = {}

# Categorías por palabras clave
topics = {
    "Mars": ["mars", "perseverance", "rover"],
    "SpaceX": ["spacex", "elon musk", "falcon", "starship"],
    "NASA": ["nasa", "hubble", "artemis", "moon", "apollo"],
    "Astronomy": ["black hole", "galaxy", "telescope", "exoplanet"]
}

def fetch_data(endpoint: str, limit: int, offset: int):
    url = f"{BASE_URL}/{endpoint}/?limit={limit}&offset={offset}"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Error en la solicitud a {url}: {e.response.status_code} - {e.response.text}")
        return {"error": "Error en la solicitud a la API"}
    except httpx.RequestError as e:
        logging.error(f"Error de conexión: {e}")
        return {"error": "Error de conexión con la API"}

def classify_article(title: str, summary: str):
    """Clasifica un artículo en un tema según palabras clave."""
    text = f"{title} {summary}".lower()
    for topic, keywords in topics.items():
        if any(keyword in text for keyword in keywords):
            return topic
    return "Other"

def process_articles(articles):
    """Deduplicación y clasificación de artículos."""
    processed = []
    for article in articles.get("results", []):
        article_id = article["id"]
        if article_id not in db_articles:
            category = classify_article(article["title"], article["summary"])
            article["category"] = category
            db_articles[article_id] = article
            processed.append(article)
    return processed

@app.get("/articles")
def get_articles(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    time.sleep(RATE_LIMIT)
    data = fetch_data("articles", limit, offset)
    return process_articles(data)

@app.get("/blogs")
def get_blogs(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    time.sleep(RATE_LIMIT)
    data = fetch_data("blogs", limit, offset)
    return process_articles(data)

@app.get("/reports")
def get_reports(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    time.sleep(RATE_LIMIT)
    data = fetch_data("reports", limit, offset)
    return process_articles(data)

@app.get("/info")
def get_info():
    return fetch_data("", 1, 0)
