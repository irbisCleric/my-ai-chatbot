import psycopg2
from psycopg2.extras import RealDictCursor

## DB connect
DB_NAME = "mydatabase"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    try:
        conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )
        return conn
    except Exception as e:
        print(f"Error connection to DB: {e}")
        return None

def create_table():
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("✅ Table created!")
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error during creating table: {e}")

# Check connection
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("✅ Successful connected to DB!")
        conn.close()
    else:
        print("❌ Issue during DB connect.")
    create_table()
