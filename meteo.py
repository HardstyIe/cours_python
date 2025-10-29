from openai import OpenAI
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openweather_api_key = os.getenv("WEATHER_API_KEY")

# Tool météo qu’on va exposer à l’IA
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a given city using OpenWeatherMap API",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City to get the weather from",
                },
            },
            "required": ["city"],
        },
    }
]

# Fonction qui récupère les données météo depuis OpenWeatherMap
def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=metric&lang=fr"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Ville '{city}' introuvable ou erreur API."}

    data = response.json()
    return {
        "city": city,
        "temperature": f"{data['main']['temp']}°C",
        "feels_like": f"{data['main']['feels_like']}°C",
        "condition": data['weather'][0]['description'].capitalize(),
        "humidity": f"{data['main']['humidity']}%",
        "wind_speed": f"{data['wind']['speed']} m/s",
    }

# Je demande la ville à l’utilisateur
city_name = input("Entre une ville : ").strip()
input_list = [{"role": "user", "content": f"Donne-moi la météo actuelle à {city_name}."}]

# Premier appel : GPT décide s’il doit utiliser la fonction météo
response = client.responses.create(
    model="gpt-5-mini",
    tools=tools,
    input=input_list,
)

# J’ajoute la sortie du modèle dans la conversation
input_list += response.output

# Si GPT appelle le tool, je l’exécute ici
for item in response.output:
    if item.type == "function_call" and item.name == "get_weather":
        args = json.loads(item.arguments)
        weather_data = get_weather(args["city"])

        # Je renvoie le résultat brut de l’API à GPT
        input_list.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps(weather_data),
        })

# Deuxième appel : GPT reformule le résultat en français naturel
response = client.responses.create(
    model="gpt-5-mini",
    instructions="Réponds comme un bulletin météo en français, à partir des données fournies par le tool.",
    tools=tools,
    input=input_list,
)

# Affichage du résultat final
print("\n--- Météo ---")
print(response.output_text)
