from fastapi import FastAPI, Query
import httpx

app = FastAPI()
BASE_URL = "https://api.spaceflightnewsapi.net/v4"

def fetch_data(endpoint: str, limit: int, offset: int):
    url = f"{BASE_URL}/{endpoint}/?limit={limit}&offset={offset}"
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()

@app.get("/articles")
def get_articles(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    return fetch_data("articles", limit, offset)

@app.get("/blogs")
def get_blogs(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    return fetch_data("blogs", limit, offset)

@app.get("/reports")
def get_reports(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    return fetch_data("reports", limit, offset)

@app.get("/info")
def get_info():
    response = httpx.get(BASE_URL)
    response.raise_for_status()
    return response.json()
