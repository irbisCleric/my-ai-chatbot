import mysql.connector
from mysql.connector import Error

def connect_to_db():
    """Function to connect to the database."""
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
    """Function to insert a message into the table."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO messages (sender, message) VALUES (%s, %s)"
        cursor.execute(query, (sender, message))
        connection.commit()
        print("Message inserted successfully")
        cursor.close()
        connection.close()

def get_messages():
    """Function to retrieve all messages from the table."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM messages"
        cursor.execute(query)
        records = cursor.fetchall()
        print("All messages:")
        for record in records:
            print(f"ID: {record[0]}, Sender: {record[1]}, Message: {record[2]}, Sent at: {record[3]}")
        cursor.close()
        connection.close()

# Example usage:
# Inserting a message
insert_message('Chatbot', 'Hello! How can I assist you today?')

# Retrieving all messages
get_messages()
