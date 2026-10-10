
# import oracledb
# import config

# # ADD THIS LINE: Tells the driver to return CLOBs as strings automatically
# oracledb.defaults.fetch_lobs = False 

# def get_connection():
#     try:
#         conn = oracledb.connect(
#             user=config.DB_USER,
#             password=config.DB_PASSWORD,
#             dsn=config.DB_DSN,
#             config_dir=config.WALLET_DIR,
#             wallet_location=config.WALLET_DIR,
#             wallet_password=config.WALLET_PASSWORD
#         )
#         print("✅ Connection Successful to Oracle 23ai")
#         return conn
#     except oracledb.Error as e:
#         print(f"❌ Connection Error: {e}")
#         return None
import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Establishes and returns an Oracle database connection."""
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=os.getenv("DB_DSN"),
        config_dir=os.getenv("WALLET_DIR"),
        wallet_location=os.getenv("WALLET_DIR"),
        wallet_password=os.getenv("WALLET_PASSWORD")
    )



# import os
# import oracledb
# from dotenv import load_dotenv

# load_dotenv()

# def get_connection():
#     return oracledb.connect(
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         dsn=os.getenv("DB_DSN"),
#         config_dir=os.getenv("WALLET_DIR"),
#         wallet_location=os.getenv("WALLET_DIR"),
#         wallet_password=os.getenv("WALLET_PASSWORD")
#     )

# def create_user(username, email, password_hash):
#     """Inserts a new user record into the Oracle database."""
#     conn = None
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()
        
#         # SQL query using exact column names matching your USERS table
#         sql = """
#             INSERT INTO users (username, email, password_hash)
#             VALUES (:1, :2, :3)
#         """
#         cursor.execute(sql, (username, email, password_hash))
#         conn.commit()
#         cursor.close()
#         print(f"User {username} created successfully!")
#         return True
#     except oracledb.DatabaseError as e:
#         if conn:
#             conn.rollback()
#         error, = e.args
#         print(f"❌ Signup Error (ORA-{error.code:05d}): {error.message}")
#         raise e
#     finally:
#         if conn:
#             conn.close()

# import oracledb

# @app.route('/signup', methods=['POST'])
# def signup():
#     username = request.form.get('name')
#     email = request.form.get('email')
#     password = request.form.get('password')
#     hashed_pw = hash_password(password)
    
#     conn = get_connection()
#     if not conn: 
#         return "❌ DB Connection Error"
        
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO users (username, email, password_hash) VALUES (:1, :2, :3)", 
#             [username, email, hashed_pw]
#         )
#         conn.commit()
#         return redirect(url_for('index'))
#     except oracledb.DatabaseError as e:
#         error, = e.args
#         if error.code == 1:  # ORA-00001: Unique constraint error
#             return "❌ An account with this email already exists. Please log in.", 400
#         return f"❌ Signup Error: {error.message}", 400
#     except Exception as e:
#         return f"❌ Signup Error: {e}", 400
#     finally:
#         cursor.close()
#         conn.close()