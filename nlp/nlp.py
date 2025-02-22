from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Loads API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_entities(dream_text):
    system_message = "Entities are defined as people, places, objects, and emotions in the context. Extract the key entities from the following text.  Return a JSON object with a single key called 'entities'. The value of this key should be a JSON array containing the entities."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": dream_text}
        ],
        temperature=1.0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Parse the response to extract the entities
    content = response.choices[0].message.content
    data = json.loads(content)
    entities = data["entities"]
    return entities

def analyze_sentiment(dream_text):
    system_message = "Analyze the sentiment of the following text. Return a JSON object with a single key called 'sentiment'. The value of this key should be a string indicating the sentiment (positive, negative, neutral)."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": dream_text}
        ],
        temperature=1.0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Parse the response to extract the sentiment
    content = response.choices[0].message.content
    data = json.loads(content)
    sentiments = data["sentiment"]
    return sentiments

def interpret_symbols(dream_text):
    system_message = "Interpret the symbols in the following text. Return a JSON object with a single key called 'interpretation'. The value of this key should be a string containing the interpretation of the symbols."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": dream_text}
        ],
        temperature=1.0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Parse the response to extract the interpretation
    content = response.choices[0].message.content
    data = json.loads(content)
    interpretation = data["interpretation"]
    return interpretation

def analyze_dream(dream_text):
    entities = extract_entities(dream_text)
    sentiment = analyze_sentiment(dream_text)
    interpretation = interpret_symbols(dream_text)
    
    nlp_output = {
        "entities": entities,
        "sentiment": sentiment,
        "interpretation": interpretation
    }
    return nlp_output
