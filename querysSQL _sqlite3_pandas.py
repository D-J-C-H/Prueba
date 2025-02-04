# Probando la version de sqlite
#import sqlite3
#print(sqlite3.sqlite_version)


import sqlite3
import pandas as pd

# Cargar el CSV en un DataFrame
df = pd.read_csv("processed_news.csv")

import ast


df["keywords"] = df["keywords"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")




# Conectar a SQLite (crea la base si no existe)
conn = sqlite3.connect("news_database.db")

# Guardar el DataFrame en SQLite
df.to_sql("processed_news", conn, if_exists="replace", index=False)

# Definir y ejecutar consultas SQL
queries = {
    "Tendencias de temas por mes": 
        "SELECT strftime('%Y-%m', published_at) AS month, category, COUNT(*) AS article_count FROM processed_news GROUP BY month, category ORDER BY month DESC, article_count DESC;",
    
    "Fuentes más influyentes": 
        "SELECT news_site, COUNT(*) AS total_articles FROM processed_news GROUP BY news_site ORDER BY total_articles DESC LIMIT 10;",
    
    #"Autores más activos":
    #    "SELECT json_extract(authors, '$[0].name') AS author, COUNT(*) AS total_articles FROM processed_news WHERE author IS NOT NULL GROUP BY author ORDER BY total_articles DESC LIMIT 10;",

    
    #"Palabras clave más frecuentes":
    #    "SELECT word, COUNT(*) AS word_count FROM (SELECT LOWER(value) AS word FROM processed_news, json_each(replace(replace(replace(keywords, '[', ''), ']', ''), '\"', '')))GROUP BY word ORDER BY word_count DESC LIMIT 10;"
}

# Ejecutar y mostrar los resultados
for title, query in queries.items():
    print(f"\n📌 {title}:")
    result = pd.read_sql_query(query, conn)
    print(result)

# Cerrar conexión
conn.close()
