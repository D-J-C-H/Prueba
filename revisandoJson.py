import json

with open("c:/Users/deyvi.caicedo/Documents/GitHub/Prueba/json_files/response_1738639677530.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print("Claves en el JSON:", data[0].keys())  # Muestra las claves del primer artículo
