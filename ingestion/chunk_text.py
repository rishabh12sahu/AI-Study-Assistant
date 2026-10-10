def chunk_text(text, chunk_size=700, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        # The 'overlap' makes sure the end of one chunk is the start of the next
        start += (chunk_size - overlap) 
    return chunks
