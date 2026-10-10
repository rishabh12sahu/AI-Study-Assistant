from openai import OpenAI
from config import OPENAI_API_KEY
from tqdm import tqdm

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "text-embedding-3-large"

def generate_embeddings(chunks, batch_size=10):
    embeddings = []
    clean_chunks = [c.strip() for c in chunks if c and c.strip()]

    for i in tqdm(range(0, len(clean_chunks), batch_size), desc="Embedding chunks"):
        batch = clean_chunks[i:i+batch_size]
        response = client.embeddings.create(model=MODEL, input=batch)
        for item in response.data:
            embeddings.append(item.embedding)
    return embeddings

def embed_query(query):
    """Generates embedding for a single user query."""
    response = client.embeddings.create(model=MODEL, input=query)
    return response.data[0].embedding