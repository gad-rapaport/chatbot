import requests
import os
import json
from dotenv import load_dotenv

# טעינת משתנים
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL", "https://openrouter.ai/api/v1/chat/completions")
BOT_MODEL = os.getenv("BOT_MODEL", "google/gemini-2.0-flash-001")

def get_bot_response(user_input):
    # בדיקה קריטית - האם המפתח נטען?
    if not API_KEY:
        return "System Error: API_KEY not found. Please check your .env file."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:3000",
        "X-Title": "My Python Chatbot"
    }
    
    payload = {
        "model": BOT_MODEL,
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"
            
        data = response.json()
        
        if 'choices' in data and len(data['choices']) > 0:
            return data['choices'][0]['message']['content']
        else:
            return "Error: Empty response from API"

    except Exception as e:
        return f"System Error: {str(e)}"
