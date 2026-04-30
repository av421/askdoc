from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
model = SentenceTransformer(MODEL_NAME)

def embed_chunks(chunks: List[Dict]) -> List[Dict]:
    
    print(f'Embedding {len(chunks)} chunks with model: {MODEL_NAME}')

    texts = [chunk['text'] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    for chunk, embedding in zip(chunks, embeddings):
        chunk['embedding'] = embedding.tolist()

    print('Embedding complete!')
    return chunks

def embed_query(query: str) -> List[float]:
    return model.encode(query).tolist()

