import asyncio
import aiohttp
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI()

openai_api_key = os.getenv('OPENAI_API_KEY')

async def get_ai_response(prompt: str,name: str):
    """
    Envoie le prompt à l'API OpenAI pour une IA donnée.
    
    Args:
        prompt (str): L'historique ou le message auquel l'IA doit répondre.
        role_name (str): Nom ou rôle de l'IA (ex: "IA1" ou "IA2").
    
    Returns:
        str: Le texte de la réponse générée par l'IA.
    """

    response = client.responses.create(
    model="gpt-4.1-mini",
    instructions=f"{name} répond de maniere consise (petit texte) au message",
    input=prompt
    )
    return response.output_text

history = []
ia1_name = "IA1"
ia2_name = "IA2"

# Message initial de IA1
initial_msg = "on va parler d'un sujet politique"
print(f"{ia1_name}: {initial_msg}\n")

try:
    while True:
        
        # IA2 répond
        prompt_ia2 = "\n".join(history) or initial_msg
        response_ia2 = asyncio.run(get_ai_response(prompt_ia2, ia2_name))
        history.append(f"{ia2_name}: {response_ia2}")
        print(f"{ia2_name}: {response_ia2}\n")

        # IA1 répond
        prompt_ia1 = "\n".join(history) or initial_msg
        response_ia1 = asyncio.run(get_ai_response(prompt_ia1, ia1_name)) 
        history.append(f"{ia1_name}: {response_ia1}")
        print(f"{ia1_name}: {response_ia1}\n")

except KeyboardInterrupt:
    print("Conversation interrompue par l'utilisateur.")