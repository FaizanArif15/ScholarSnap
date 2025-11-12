# db.py
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime   
import pytz

karachi_tz = pytz.timezone("Asia/Karachi")

def get_connection():
    """Securely create a PostgreSQL connection using environment variables."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            cursor_factory=RealDictCursor
        )
        with conn.cursor() as cur:
            cur.execute("SET TIMEZONE TO 'Asia/Karachi';")
        print("✅ Database connected successfully!")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None
    
    
def init_db():
    """Create table if not exists."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id SERIAL PRIMARY KEY,
                sent_at TIMESTAMP NOT NULL DEFAULT NOW(),
                email TEXT,
                paper_title TEXT,
                paper_url TEXT,
                summary TEXT
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database Created successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    return True


def email_sent_today(email):
    """
    Returns True if the given email already has a log entry with sent_at today (Asia/Karachi timezone).
    """
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        # Compare only date part
        cur.execute(
            """
            SELECT 1
            FROM logs
            WHERE email = %s
              AND sent_at::date = CURRENT_DATE;
            """,
            (email,)
        )
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"❌ Failed to check email_sent_today: {e}")
        return False



def log_email_sent(email, paper_title, paper_url, summary=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO logs (sent_at, email, paper_title, paper_url, summary) VALUES (%s, %s, %s, %s, %s);",
            (datetime.now(karachi_tz), email, paper_title, paper_url, summary),
        )
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Data Inserted successfully!")
    except Exception as e:
        print(f"❌ Logging email failed: {e}")
        return False
    return True 