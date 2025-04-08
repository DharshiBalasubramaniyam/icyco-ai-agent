from datetime import time
import os
import re

from dotenv import load_dotenv
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()


def get_vector_store(pc_index_name):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    embedding_model = getEmbeddingModel()
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if pc_index_name not in existing_indexes:
        create_vector_store(pc, pc_index_name, embedding_model)

    index = pc.Index(pc_index_name)
    return PineconeVectorStore(index=index, embedding=embedding_model)


def create_vector_store(pc, pc_index_name, embedding_model):
    pc.create_index(
        name=pc_index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    while not pc.describe_index(pc_index_name).status['ready']:  
        time.sleep(1)
    index = pc.Index(pc_index_name)
    vector_store = PineconeVectorStore(index=index, embedding=embedding_model)
    pdf_files = [file for root, _, files in os.walk("resources") for file in files if file.lower().endswith(".pdf")]
    add_documents_to_vector_store(vector_store, pdf_files)
    return vector_store


def getTextSplitter():
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    return text_splitter


def getEmbeddingModel():
    embedding_model = FastEmbedEmbeddings()
    return embedding_model


def getLLM():
    api_key = os.getenv("GOOGLE_API_KEY")
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
    return llm

def createRagChain(llm, vector_store, prompt_template):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),  # Selects the top 3 most relevant chunks
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template},
    )
    return qa_chain


def create_chunks(file_path):
    loader = PyPDFLoader(f"resources/{file_path}")
    documents = loader.load()  # Load all pages of the pdf

    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    chunked_docs = getTextSplitter().split_documents(documents)
    return chunked_docs


def add_documents_to_vector_store(vector_store, pdfs):
    chunks = []
    for pdf in pdfs:
        chunks.extend(create_chunks(pdf))
    vector_store.add_documents(chunks)


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()