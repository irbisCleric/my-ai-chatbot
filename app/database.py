import mysql.connector
from mysql.connector import Error
import openai
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def connect_to_db():
    """Connect to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='chatbot_user',
            password='your_password',
            database='chatbot_db'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_message(sender, message):
    """Insert message into the database."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO messages (sender, message) VALUES (%s, %s)"
        cursor.execute(query, (sender, message))
        connection.commit()
        print("Message inserted successfully")
        cursor.close()
        connection.close()

def get_ai_response(prompt):
    """Get response from OpenAI model."""
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

def chatbot_conversation(user_message):
    """Handle chatbot conversation."""
    # Save user's message to database
    insert_message('User', user_message)
    
    # Get AI response
    ai_message = get_ai_response(user_message)
    
    # Save AI's response to database
    insert_message('Chatbot', ai_message)
    
    return ai_message

# Example usage
user_input = "Hello, how are you?"
ai_reply = chatbot_conversation(user_input)
print(ai_reply)
