import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = 'gpt-4o-mini'

EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')

CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './data/chroma_db')
DEFAULT_COLLECTION = 'documents'

# Chunking
DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 50

# Retrieval
DEFAULT_TOP_K = 5