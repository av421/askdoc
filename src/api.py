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

