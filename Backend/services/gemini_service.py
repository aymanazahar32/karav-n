# services/gemini_service.py

import requests
from flask import current_app

def get_ai_recommendation(prompt_text):
    """
    Send prompt to Gemini (or other LLM) and retrieve structured suggestion.
    This is a MOCK function – replace with actual code to call your LLM.
    """
    api_key = current_app.config["GEMINI_API_KEY"]
    if not api_key:
        return "AI Recommendation is unavailable because GEMINI_API_KEY is missing."
    
    try:
        # Pseudocode for a hypothetical request:
        # url = "https://api.gemini.com/v1/complete"
        # headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        # payload = {"prompt": prompt_text, "max_tokens": 256}
        # response = requests.post(url, json=payload, headers=headers)
        # data = response.json()
        # recommended_response = data["choices"][0]["text"]
        recommended_response = "Based on user preferences, the best campsite is Mock Campground A, enjoy stargazing!"
        return recommended_response
    except Exception as e:
        print(f"Gemini AI error: {e}")
        return "AI recommendation service encountered an error."
