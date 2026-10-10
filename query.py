from ingestion.generate_embedding import embed_query
from database.search_oracle import search_chunks
from llm import ask_llm

def main():
    while True:
        # STEP 1: Interactive Input
        user_question = input("\n💬 Enter your question (or type 'exit' to quit): ")
        
        if user_question.lower() == 'exit':
            break

        print(f"🔍 Searching for answers...")
        
        # STEP 2: Vectorize
        query_embedding = embed_query(user_question)

        # STEP 3: Search DB
        results = search_chunks(query_embedding, top_k=6)
        
        # # --- DEBUG START: Add this here ---
        # print(f"DEBUG: Found {len(results)} relevant text segments.")
        # for i, text in enumerate(results):
        #     print(f"--- Chunk {i+1} Preview ---")
        #     if text:
        #         print(text[:300]) # Show first 300 characters
        #     else:
        #         print("[ERROR: THIS CHUNK IS EMPTY OR NULL]")
        # print("-" * 30)
        # --- DEBUG END ---

        if not results:
            print("📭 No information found in the database. Try running main.py again.")
            continue

        # STEP 4: Get Answer from LLM
        context = "\n---\n".join(results)
        answer = ask_llm(user_question, context)

        print("\n" + "="*60)
        print("🤖 AI RESPONSE:")
        print(answer)
        print("="*60 + "\n")

if __name__ == "__main__":
    main()
