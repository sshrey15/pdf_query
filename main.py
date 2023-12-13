import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import  CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from langchain.vectorstores import FAISS



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts = text_chunks, embeddings = embeddings)
    return vectorstore

   


def main():
    load_dotenv()
    st.set_page_config(page_title="Streamlit App", page_icon=":shark:", layout="wide")
    st.header("Chat with multiple pdfs at once :books:")
    st.text_input("Ask any question about about your pdfs")

    pdf_docs = None
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your pdfs here and click on process", type=["pdf"], accept_multiple_files=True)
    if pdf_docs and st.button("Process"):
        with st.spinner("Processing..."):
            raw_text = get_pdf_text(pdf_docs)
            

            text_chunks =  get_text_chunks(raw_text)    
            st.write(text_chunks)
            st.success("Done!") 

            vectorstore = get_vectorstore(text_chunks)
            st.write(vectorstore)
          


if  __name__ == '__main__':
    main()
