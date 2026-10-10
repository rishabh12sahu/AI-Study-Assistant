# from database.oracle_db import get_connection
# import array

# def search_chunks(query_embedding, top_k=3):
#     conn = get_connection()
#     if not conn: return []
#     cursor = conn.cursor()
#     try:
#         # Convert list to array for Oracle 23ai
#         query_vec = array.array('d', query_embedding)
        
#         cursor.execute(
#             """
#             SELECT text
#             FROM vector_store
#             ORDER BY embedding <=> TO_VECTOR(:1)
#             FETCH FIRST :2 ROWS ONLY
#             """,
#             [query_vec, top_k]
#         )
        
#         results = []
#         for row in cursor.fetchall():
#             item = row[0]
#             # Check if it's a LOB and read it, or convert to string
#             if hasattr(item, 'read'):
#                 results.append(item.read())
#             else:
#                 results.append(str(item))
        
#         return results

#     except Exception as e:
#         print(f"❌ Search Error: {e}")
#         return []
#     finally:
#         cursor.close()
#         conn.close()




# database/search_oracle.py
import array
# THIS LINE MUST BE HERE:
from database.oracle_db import get_connection 

def search_chunks(query_embedding, user_email, top_k=6):
    if not user_email:
        return []

    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query_vec = array.array('d', query_embedding)
        user_email = user_email.strip().lower()

        # Named parameters to prevent ORA-00932
        sql = """
            SELECT text
            FROM vector_store
            WHERE user_email = :email
            ORDER BY embedding <=> TO_VECTOR(:vec)
            FETCH FIRST :k ROWS ONLY
        """
        
        params = {
            "email": user_email,
            "vec": query_vec,
            "k": top_k
        }

        cursor.execute(sql, params)
        
        results = []
        for row in cursor.fetchall():
            item = row[0]
            if hasattr(item, 'read'):
                results.append(item.read())
            else:
                results.append(str(item))
        
        return results
    except Exception as e:
        print(f"❌ Search Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()