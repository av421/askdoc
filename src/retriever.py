import chromadb
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './data/chroma_db')


def get_client():
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_or_create_collection(collection_name='documents'):
    client = get_client()
    return client.get_or_create_collection(
        name=collection_name,
        metadata={'hnsw:space': 'cosine'}
    )


def store_chunks(chunks, collection_name='documents'):
    collection = get_or_create_collection(collection_name)

    ids = [f'chunk_{chunk["chunk_index"]}' for chunk in chunks]
    embeddings = [chunk['embedding'] for chunk in chunks]
    documents = [chunk['text'] for chunk in chunks]
    metadatas = [
        {
            'chunk_index': chunk['chunk_index'],
            'start_char': chunk['start_char'],
            'end_char': chunk['end_char']
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print(f'Stored {len(chunks)} chunks in collection {collection_name}')


def retrieve_relevant_chunks(query_embedding, collection_name='documents', top_k=5):
    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results['documents'][0]