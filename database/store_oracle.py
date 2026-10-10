# from database.oracle_db import get_connection
# from tqdm import tqdm
# import array

# def store_embeddings(chunks, embeddings, batch_size=50):
#     conn = get_connection()
#     if not conn: return
    
#     cursor = conn.cursor()
#     try:
#         # 1. Clear old data to avoid duplicates
#         print("🧹 Clearing old data...")
#         cursor.execute("TRUNCATE TABLE vector_store")

#         # 2. Store new data
#         for text, vector in tqdm(zip(chunks, embeddings), total=len(chunks), desc="Storing in Oracle"):
#             # Oracle 23ai requires double array for VECTOR column
#             vec_array = array.array('d', vector)
#             cursor.execute(
#                 "INSERT INTO vector_store (text, embedding) VALUES (:1, TO_VECTOR(:2))",
#                 [text, vec_array]
#             )
        
#         conn.commit()
#         print(f"✅ Successfully stored {len(chunks)} chunks.")
#     except Exception as e:
#         print(f"❌ Storage Error: {e}")
#         conn.rollback()
#     finally:
#         cursor.close()
#         conn.close()




# database/store_oracle.py
import array
from tqdm import tqdm
# THIS LINE WAS MISSING:
from database.oracle_db import get_connection 

def store_embeddings(chunks, embeddings, user_email):
    if not user_email:
        print("❌ ERROR: No user email provided!")
        return

    conn = get_connection()
    if not conn: return
    
    cursor = conn.cursor()
    try:
        user_email = user_email.strip().lower()
        
        # 1. Clear ONLY this specific user's old data
        print(f"🧹 Clearing old data for user: {user_email}")
        cursor.execute("DELETE FROM vector_store WHERE user_email = :1", [user_email])

        # 2. Store new data using named parameters for safety
        for text, vector in tqdm(zip(chunks, embeddings), total=len(chunks), desc="Storing"):
            vec_array = array.array('d', vector)
            cursor.execute(
                """
                INSERT INTO vector_store (text, embedding, user_email) 
                VALUES (:txt, TO_VECTOR(:vec), :email)
                """,
                {"txt": text, "vec": vec_array, "email": user_email}
            )
        
        conn.commit()
        print(f"✅ Successfully stored data for {user_email}")
    except Exception as e:
        print(f"❌ Storage Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()