# services/gemini_service.py

import requests
from flask import current_app
from functools import lru_cache
import time

@lru_cache(maxsize=50)
def get_ai_recommendation(prompt_text):
    """
    Send prompt to Gemini API and retrieve structured recommendation.
    Cached for 1 hour to avoid excessive API calls.
    """
    api_key = current_app.config["GEMINI_API_KEY"]
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured")
    
    try:
        url = current_app.config["GEMINI_API_URL"]
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt_text,
            "max_tokens": 256,
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract the recommendation text
        recommendation = data.get("choices", [{}])[0].get("text", "").strip()
        
        return {
            "text": recommendation,
            "timestamp": int(time.time())
        }
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Gemini API error: {str(e)}")
        return {
            "text": "AI recommendation service is currently unavailable.",
            "timestamp": int(time.time())
        }
    except (KeyError, ValueError) as e:
        current_app.logger.error(f"Gemini data parsing error: {str(e)}")
        return {
            "text": "Unable to generate AI recommendation at this time.",
            "timestamp": int(time.time())
        }
