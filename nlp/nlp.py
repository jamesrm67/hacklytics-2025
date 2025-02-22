import openai
from dotenv import load_dotenv
import os

# Loads API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_entities(dream_text):
    prompt = f"Extract the entites (people, places, objects, emotions) from the following dream text:\n\n{dream_text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    entites = response.choices[0].text.strip()
    return entites

