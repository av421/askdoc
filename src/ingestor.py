import fitz
from pathlib import Path
from typing import List, Dict

def load_pdf(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f'No file found at {file_path}')
    if path.suffix.lower() != '.pdf':
        raise ValueError(f'Expected a PDF file, got {path.suffix}')
    
    doc = fitz.open(file_path)
    full_text = ''
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append({
                'text': chunk.strip(),
                'chunk_index': chunk_index,
                'start_char': start,
                'end_char': end
            })
            chunk_index += 1

        start += chunk_size - overlap

    return chunks

def ingest_pdf(file_path: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    
    print(f'Loading PDF: {file_path}')
    text = load_pdf(file_path)
    print(f'Extracted {len(text)} characters')

    chunks = chunk_text(text, chunk_size, overlap)
    print(f'Created {len(chunks)} chunks')

    return chunks