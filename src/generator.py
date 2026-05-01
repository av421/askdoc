from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


def get_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def build_prompt(query, chunks):
    context = '\n\n---\n\n'.join(chunks)
    prompt = f'''You are a helpful assistant that answers questions based strictly on the provided document context.
If the answer is not found in the context, say "I couldn't find that in the provided documents."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:'''
    return prompt


def generate_answer(query, chunks):
    client = get_client()
    if not client:
        return 'OpenAI API key not set. Please add it to your .env file.'

    prompt = build_prompt(query, chunks)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()