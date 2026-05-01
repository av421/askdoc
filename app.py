import streamlit as st
import requests

API_URL = 'http://localhost:8000'

st.set_page_config(page_title='AskDoc', layout='centered')

st.title('AskDoc')
st.subheader('Upload a PDF document and ask questions about its content.')

with st.sidebar:
    st.header('Settings')
    collection_name = st.text_input('Collection Name', value='documents')
    top_k = st.slider('Number of chunks to retrieve', min_value=1, max_value=10, value=5)
    st.markdown('---')
    st.markdown('Using FastAPI + ChromaDB + OpenAI')



st.markdown('### Upload PDF Document')
uploaded_file = st.file_uploader('Choose a PDF file', type='pdf')

if uploaded_file is not None:
    if st.button('Ingest Document'):
        with st.spinner('Ingesting document...'):
            response = requests.post(
                f'{API_URL}/upload',
                files={'file': (uploaded_file.name, uploaded_file, 'application/pdf')},
                params={'collection_name': collection_name}
            )
        if response.status_code == 200:
            data = response.json()
            st.success(f'Ingested {data["chunks_stored"]} chunks from {uploaded_file.name}')
        else:
            st.error(f'Error: {response.text}')
    


st.markdown('### Ask Questions')
question = st.text_input('Enter your question about the document', placeholder='What is this document about?')

if st.button('Ask'):
    if not question:
        st.warning('Please enter a question.')
    else:
        with st.spinner('Retrieving answer...'):
            response = requests.post(
                f'{API_URL}/query',
                json={'question': question, 'collection_name': collection_name, 'top_k': top_k}
            )
        if response.status_code == 200:
            data = response.json()
            st.markdown('**Answer:**')
            st.write(data['answer'])

            with st.expander('Source Chunks'):
                for i, chunk in enumerate(data['sources']):
                    st.markdown(f'**Chunk {i+1}:**')
                    st.write(chunk)
                    st.markdown('---')
        
        else:
            st.error(f'Error: {response.text}')