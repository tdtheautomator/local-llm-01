import re
#import ollama
import gradio as gr
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings,ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


embedding_model = "mxbai-embed-large"
llm_model = "llama3.2:1b"


def load_vectordb(embedding_model):
    embeddings = OllamaEmbeddings(model=embedding_model)
    vector_db = Chroma(persist_directory="./embeddings", embedding_function=embeddings,collection_name="demo")
    retriever = vector_db.as_retriever()
    return retriever


def ollama_llm(query, context,llm_model):
    prompt = PromptTemplate(
    template=""""You are a helpful assistant.to provide accurate information only based on documents, 
    and if you don't know the answer from the document, please say 'I don't know!!!'"
    Question: {query}
    Documents: {context}
    Answer:
    """,
    input_variables=["query", "context"],
    )
    llm = ChatOllama(
    model=llm_model,
    temperature=0,
    )
    rag_chain = prompt | llm | StrOutputParser()
    answer = rag_chain.invoke({"query": query, "context": context})
    final_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
    return final_answer

def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def process_query(query,embedding_model,llm_model):
    retriever = load_vectordb(embedding_model)
    retrieved_docs = retriever.invoke(query)
    formatted_content = combine_docs(retrieved_docs)
    return ollama_llm(query, formatted_content,llm_model)

interface = gr.Interface(
   fn=process_query,
   inputs=[
       gr.Textbox(
           lines=2,
           label="Question",
       ),
       gr.Dropdown(choices=["mxbai-embed-large"], label="Select Embedding Model"),
       gr.Dropdown(choices=["llama3.2:1b", "deepseek-r1:1.5b", "deepseek-r1"], label="Select LLM Model"),
   ],
   outputs=gr.Textbox(
       label="Answer", 
       lines = 10,
       show_copy_button=True
       ),
   title="Chatbot for PDF",
)
interface.launch()