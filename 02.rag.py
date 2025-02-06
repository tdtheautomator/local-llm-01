
import re
import ollama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

query = "What is Energy?"
embedding_model = "mxbai-embed-large"
llm_model = "deepseek-r1:1.5b"

def load_vectordb(embedding_model):
    embeddings = OllamaEmbeddings(model=embedding_model)
    vector_db = Chroma(persist_directory="./embeddings", embedding_function=embeddings,collection_name="demo")
    #collection = vector_db.get()
    retriever = vector_db.as_retriever()
    return retriever

def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def ollama_llm(query, context,llm_model):
    formatted_prompt = f"Question: {query}\n\nContext: {context}"
    response = ollama.chat(model=llm_model, messages=[
         {
            "role": "system", 
            "content": "You are a helpful assistant.to provide accurate information, and if you don't know the answer, please say 'I don't know!!!'"
        },
        {
            "role": "user", 
            "content": formatted_prompt
        }
        ]
    )
    response_content = response["message"]["content"]
    final_answer = re.sub(r"<think>.*?</think>", "", response_content, flags=re.DOTALL).strip()
    return final_answer 

def rag_chain(query,embedding_model,llm_model):
    print("-"*10)
    print(f"LLM Model: {llm_model}")
    print(f"Embedding Model: {embedding_model}")
    print("-"*10)
    print("")
    print("")
    print(f"Query: {query}")
    print("")
    print("")
    print("-"*10)
    retriever = load_vectordb(embedding_model)
    retrieved_docs = retriever.invoke(query)
    formatted_content = combine_docs(retrieved_docs)
    print(formatted_content)
    return ollama_llm(query, formatted_content,llm_model)      


rag_chain(query,embedding_model,llm_model) 