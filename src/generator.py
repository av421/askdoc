from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def build_prompt(query: str, context: List[str]) -> str:
    
    context = '\n\n---\n\n'.join(context_chunks)
    prompt = f"""You are a helpful assistant that answers questions strictly based on the provided document context.
    If the answer is not found in the context, respond with "I don't know". Do not provide any information that is not explicitly stated in the provided documents."

    CONTEXT: 
    {context}

    QUESTION:
    {query}

    ANSWER: """

    return prompt

def generate_answer(query: str, context_chunks: List[str]) -> str:

    if not os.getenv('OPENAI_API_KEY'):
        return 'OpenAI API key issue. Please set the OPENAI_API_KEY environment variable.'
    
    prompt = build_prompt(query, context_chunks)

    response = client.chat.completions.create(
        model='gpt-4.0-mini',
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()