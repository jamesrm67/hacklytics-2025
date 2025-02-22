from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Loads API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_entities(dream_text):
    if not dream_text:
        return ("No dream text provided", 400)
    
    system_message = "Entities are defined as people, places, objects, and emotions in the context. You are a dream interpretation expert. Extract the key entities from the following dream description.  Return a JSON object with a single key called 'entities'. The value of this key should be a JSON array containing the entities."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": dream_text}
        ],
        temperature=1.0,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Parse the response to extract the entities
    content = response.choices[0].message.content
    data = json.loads(content)
    if "entities" not in data or data["entities"] == []:
        return ("No entities found", 400)
    
    entities = data["entities"]
    return entities

def analyze_sentiment(dream_text):
    if not dream_text:
        return ("No dream text provided", 400)
    
    system_message = "You are a dream interpretation expert. Analyze the sentiment of the following dream description. Return a JSON object with a single key called 'sentiment'. The value of this key should be a tuple containin a string and floating point integer indicating the sentiment (positive, negative, neutral) with the floating point integer indicating the level of sentiment from 0.0 to 1.0."
    try:
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

        if not response or 'choices' not in response or not response.choices:
            return("API response invalid or empty", 500)

        content = response.choices[0].message.content.strip() if response.choices[0].message.content else ""

        if not content:
            return ("Empty response from API", 500)

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            return (f"Invalid JSON response: {e}", 500)

        if "sentiment" not in data:
            return ("Sentiment data missing in response", 500)

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

def interpret_symbols(dream_text):
    if not dream_text:
        return ("No dream text provided", 400)
    
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
    if not dream_text:
        return ("No dream text provided", 400)
    
    entities = extract_entities(dream_text)
    sentiment = analyze_sentiment(dream_text)
    interpretation = interpret_symbols(dream_text)
    
    nlp_output = {
        "entities": entities,
        "sentiment": sentiment,
        "interpretation": interpretation
    }
    return nlp_output