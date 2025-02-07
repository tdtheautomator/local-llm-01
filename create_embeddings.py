
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

embedding_model = "mxbai-embed-large"

def create_embeddings(model_name):    
    source_files = "./docs"
    loader = DirectoryLoader(source_files, glob="./*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    embeddings = OllamaEmbeddings(model=model_name)
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="./embeddings",collection_name="demo")
    #retriever = vectorstore.as_retriever()
    return text_splitter, vectorstore


create_embeddings(embedding_model)