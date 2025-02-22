from openai import OpenAI
from database import insert_message, get_last_messages
import os
from dotenv import load_dotenv
import requests

# Loading env variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def classify_request(user_message):
    keywords = {
        "weather": ["weather", "temparature", "forecast"],
        "news": ["news", "what's new", "headers"]
    }

    user_message_lower = user_message.lower()

    for category, words in keywords.items():
        if any(word in user_message_lower for word in words):
            return category

    return "general"


def get_weather():
    API_KEY = os.getenv("WEATHER_API_KEY")
    CITY = "Amsterdam"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=en"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"Currently in {CITY} {weather_desc}, temperature {temp}°C."
        else:
            return "Can't get data about the weather"
    except Exception as e:
        return f"Error during receiving forecast: {e}"

def get_news():
    API_KEY = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            articles = data.get("articles", [])[:3]
            headlines = [f"- {article['title']}" for article in articles]
            return "Here are last news:\n" + "\n".join(headlines)
        else:
            return "Can't get data about the news"
    except Exception as e:
        return f"Error during receiving news: {e}"


def get_ai_response(prompt):
    """Get response from OpenAI model with conversation context."""
    try:
        messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        messages.extend(get_last_messages())

        messages.append({"role": "user", "content": prompt})  # Add latest user input

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def chatbot_conversation(user_message):
    """Handle chatbot conversation with context and database storage."""
    insert_message('User', user_message)  # Save user input

    category = classify_request(user_message)

    if category == "weather":
        ai_message = get_weather()
        insert_message('Chatbot', ai_message)  # Save AI response
    elif category == "news":
        ai_message = get_news()
        insert_message('Chatbot', ai_message)  # Save AI response
    else:
        ai_message = get_ai_response(user_message) # Get AI response
        insert_message('Chatbot', ai_message)  # Save AI response

    return ai_message

# Test calls
user_input = "What is the weather now?"
print(chatbot_conversation(user_input))
# user_input = "Tell me last news"
# print(chatbot_conversation(user_input))
# user_input = "How to make borscht?"
# print(chatbot_conversation(user_input))