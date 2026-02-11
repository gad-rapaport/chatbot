import requests
import os
import json
from dotenv import load_dotenv

# טעינת משתנים
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
BOT_MODEL = os.getenv("BOT_MODEL")

def get_bot_response(user_input):
    """
    שולח הודעה ל-OpenRouter ומחזיר תשובה מהמודל שנבחר.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:3000", # נדרש על ידי OpenRouter
        "X-Title": "My Python Chatbot" # שם האפליקציה שלך
    }
    
    payload = {
        "model": BOT_MODEL,
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # בדיקה אם יש שגיאה (למשל מפתח לא נכון או חוסר קרדיט)
        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"
            
        data = response.json()
        
        # חילוץ התשובה
        if 'choices' in data and len(data['choices']) > 0:
            return data['choices'][0]['message']['content']
        else:
            return "Error: Empty response from API"

    except Exception as e:
        return f"System Error: {str(e)}"
