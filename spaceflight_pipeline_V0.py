import time
import logging
import httpx
from fastapi import FastAPI, Query

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()
BASE_URL = "https://api.spaceflightnewsapi.net/v4"
RATE_LIMIT = 5  # Tiempo de espera entre peticiones para evitar bloqueos (segundos)

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

@app.get("/articles")
def get_articles(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    time.sleep(RATE_LIMIT)  # Previene bloqueos por rate limiting
    return fetch_data("articles", limit, offset)

@app.get("/blogs")
def get_blogs(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    time.sleep(RATE_LIMIT)
    return fetch_data("blogs", limit, offset)

@app.get("/reports")
def get_reports(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    time.sleep(RATE_LIMIT)
    return fetch_data("reports", limit, offset)

@app.get("/info")
def get_info():
    return fetch_data("", 1, 0)


