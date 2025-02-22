import mysql.connector
from mysql.connector import Error

def connect_to_db():
    """Connect to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='chatbot_user',
            password='mypassword',
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

def get_last_messages(limit=5):
    """Retrieve the last 'limit' messages from the database for context."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "SELECT sender, message FROM messages ORDER BY id DESC LIMIT %s"
        cursor.execute(query, (limit,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Reverse the order to maintain conversation flow
        return [{"role": "assistant" if sender == "Chatbot" else "user", "content": message} for sender, message in records][::-1]

    return []
