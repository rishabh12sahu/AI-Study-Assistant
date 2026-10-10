from database.oracle_db import get_connection
from config import DB_DSN
print("DSN VALUE:", DB_DSN)
conn = get_connection()
print("Connected successfully!")
conn.close()