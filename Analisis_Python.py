import os
import json
import pandas as pd
import spacy
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime

# Cargar modelo de NLP para análisis de entidades
nlp = spacy.load("en_core_web_sm")

# Leer múltiples archivos JSON
def load_json_files(folder_path):
    data = []
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                data.extend(json.load(f))
    return pd.DataFrame(data)

# Extraer palabras clave y entidades
def extract_entities(text):
    doc = nlp(text)
    entities = {"ORG": [], "PERSON": [], "GPE": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities

# Clasificación de artículos por tema
topics = {
    "Mars": ["mars", "perseverance", "rover"],
    "SpaceX": ["spacex", "elon musk", "falcon", "starship"],
    "NASA": ["nasa", "hubble", "artemis", "moon", "apollo"],
    "Astronomy": ["black hole", "galaxy", "telescope", "exoplanet"]
}

def classify_article(title):
    title_lower = title.lower()
    for topic, keywords in topics.items():
        if any(keyword in title_lower for keyword in keywords):
            return topic
    return "Other"

# Análisis de tendencias
def plot_trends(df):
    df["published_at"] = pd.to_datetime(df["published_at"])
    df["month"] = df["published_at"].dt.to_period("M")
    trends = df.groupby(["month", "category"]).size().unstack().fillna(0)
    trends.plot(kind="line", figsize=(10,5))
    plt.title("Tendencias de artículos por mes y categoría")
    plt.xlabel("Fecha")
    plt.ylabel("Número de artículos")
    plt.legend(title="Categoría")
    plt.show()

# Análisis de fuentes de noticias más activas
def plot_top_sources(df):
    top_sources = df["news_site"].value_counts().head(10)
    top_sources.plot(kind="bar", figsize=(10,5))
    plt.title("Fuentes de noticias más activas")
    plt.xlabel("Fuente")
    plt.ylabel("Número de artículos")
    plt.show()

# Procesamiento principal
def main():
    folder_path = "./json_files"  # Ruta donde están los archivos JSON
    df = load_json_files(folder_path)
    
    print("Columnas del DataFrame:", df.columns)
    print("Primeras filas:\n", df.head())


    # Extraer entidades
    df["entities"] = df["summary"].apply(extract_entities)
    
    # Clasificar artículos por tema
    df["category"] = df["title"].apply(classify_article)
    
    # Guardar resultados en CSV
    df.to_csv("processed_news.csv", index=False)
    
    # Mostrar gráficos de tendencias y fuentes
    plot_trends(df)
    plot_top_sources(df)
    
    print("Análisis completado. Resultados guardados en processed_news.csv")

if __name__ == "__main__":
    main()
