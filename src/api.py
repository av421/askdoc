from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
from typing import List
import tempfile

from src.ingestor import ingest_pdf
from src.embedder import embed_chunks, embed_query
from src.retriever import store_chunks, retrieve_relevant_chunks
from src.generator import generate_answer

app = FastAPI(
    title = 'askdoc API',
    description='Document Q&A using RAG',
    version='1.0.0'
)

class QueryRequest(BaseModel):
    question: str
    collection_name: str = 'documents'
    top_k: int = 5

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List

@app.get('/')
def root():
    return {'message': 'AskDoc is running...'}

@app.post('/upload')
async def upload_pdf(
    file: UploadFile = File(...),
    collection_name: str = 'documents'
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF files are supported')

    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # Full RAG ingestion pipeline
        chunks = ingest_pdf(tmp_path)
        chunks = embed_chunks(chunks)
        store_chunks(chunks, collection_name=collection_name)
    finally:
        os.unlink(tmp_path)  # clean up temp file

    return {
        'message': f'Successfully ingested {file.filename}',
        'chunks_stored': len(chunks),
        'collection': collection_name
    }


@app.post('/query', response_model=QueryResponse)
def query_documents(request: QueryRequest):
    
    query_embedding = embed_query(request.question)

    relevant_chunks = retrieve_relevant_chunks(query_embedding, collection_name=request.collection_name, top_k=request.top_k)

    if not relevant_chunks:
        raise HTTPException(status_code=404, detail='No relevant documents found')
    
    answer = generate_answer(request.question, relevant_chunks)

    return QueryResponse(
        question=request.question,
        answer=answer,
        sources=relevant_chunks
    )

@app.delete('/collection/{collection_name}')
def delete_collection(collection_name: str):
 
    from src.retriever import get_client
    client = get_client()
    client.delete_collection(collection_name)
    return {'message': f"Collection '{collection_name}' deleted"}