from ingestion.extract_pdf import extract_text
from ingestion.chunk_text import chunk_text
from ingestion.generate_embedding import generate_embeddings
from database.store_oracle import store_embeddings

text = extract_text("sample.pdf")
chunks = chunk_text(text)
# text = extract_text("sampleee.pdf")
# chunks = chunk_text(text)
print(f"Total chunks to embed: {len(chunks)}")

embeddings = generate_embeddings(chunks, batch_size=10)
store_embeddings(chunks, embeddings, batch_size=50)

print("Data stored successfully!")