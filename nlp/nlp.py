from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Loads API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_entities(dream_text):
    try:
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
        entities = data.get("entities", [])
        return entities
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from the API. Extracting entities failed.")
    except Exception as e:
        raise ValueError(f"Error extracting entities: {str(e)}")


def analyze_sentiment(dream_text):
    try:
        system_message = "You are a dream interpretation expert. Analyze the sentiment of the following dream description. Return a JSON object with a single key called 'sentiment'. The value of this key should be a tuple containing a string and floating point integer indicating the sentiment (positive, negative, neutral) with the floating point integer indicating the level of sentiment from 0.0 to 1.0."
        print("pre response")
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
        print("pre content")
        content = response.choices[0].message.content
        print("pre data")
        data = json.loads(content)
        print("pre sentiments")
        sentiments = (data.get("sentiment")[0], data.get("sentiment")[1])
        return sentiments
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from the API. Analyzing sentiment failed.")
    except Exception as e:
        raise ValueError(f"Error analyzing sentiment: {str(e)}")


def interpret_symbols(dream_text):
    try:
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
        interpretation = data.get("interpretation")
        return interpretation
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from the API. Interpreting symbols failed.")
    except Exception as e:
        raise ValueError(f"Error interpreting symbols: {str(e)}")

def analyze_dream(dream_text):
    try:
        entities = extract_entities(dream_text)
        sentiment = analyze_sentiment(dream_text)
        interpretation = interpret_symbols(dream_text)
        
        nlp_output = {
            "entities": entities,
            "sentiment": sentiment,
            "interpretation": interpretation
        }
        return nlp_output
    except Exception as e:
        return str(e)
