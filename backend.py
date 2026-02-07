#MAKE SURE .env has YOUR GROQ AND HUGGINGFACE API KEY

import os
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from pathlib import Path
import glob

#IMPORT FROM LANGGCHAIN 
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain_community.document_compressors import FlashrankRerank
from flashrank import Ranker

load_dotenv()

#UTILITIES FOR BACKEND CODE
model = ChatGroq(model="llama-3.3-70b-versatile")
low_llm = ChatGroq(model="llama-3.1-8b-instant")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=300, chunk_overlap=30)
flashrank_client = Ranker(model_name="ms-marco-MiniLM-L-12-v2")
compressor = FlashrankRerank(client=flashrank_client)
compression_retriever = None


#CODE FOR GETTING TRANSCIRPT OF YOUTUBE VIDEO FROM FRONTEND
def get_transcript_from_url(video_url: str) -> str:
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'writesubtitles': True, 
        'writeautomaticsub': True,     
        'skip_download': True, 
        'subtitleslangs': ['en.*'],     
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s'
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        video_id = info.get("id")
        search_pattern = os.path.join(output_dir, f"{video_id}.en*.vtt")
        files = glob.glob(search_pattern)
        if not files:
            raise Exception("No English subtitles or auto-captions found for this video.")
        vtt_path = files[0] 
        lines = Path(vtt_path).read_text(encoding='utf-8').splitlines()
        return " ".join([
            l.strip() for l in lines 
            if l and "-->" not in l and not l.strip().isdigit() and "WEBVTT" not in l
        ])


#STORING THE TRANSCRIPT CHUNKS INTO VECTOR EMBEDDINGS   
def update_retriever_for_url(video_url: str):
    global compression_retriever
    text = get_transcript_from_url(video_url)
    doc_splits = text_splitter.split_documents([Document(page_content=text)])
    dense = FAISS.from_documents(doc_splits, embedding_model).as_retriever(search_kwargs={"k": 5})
    sparse = BM25Retriever.from_documents(doc_splits)
    sparse.k = 5
    hybrid = EnsembleRetriever(retrievers=[dense, sparse], weights=[0.7, 0.3])
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=hybrid)


#UPDATING THE QUERY TO BE ALIGNED WITH PAST HISTORY
context_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "Formulate a standalone question based on history."),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]) | low_llm | StrOutputParser()
)

def contextualized_retriever(input_dict):
    query = context_chain.invoke(input_dict) if input_dict.get("history") else input_dict["input"]
    return compression_retriever.invoke(query)

document_chain = create_stuff_documents_chain(
    llm=model, 
    prompt=ChatPromptTemplate.from_messages([
        ("system", "Answer based ONLY on context:\n\n{context}"),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ])
)

#RAG PIPELINE
rag_pipeline = RunnablePassthrough.assign(context=contextualized_retriever) | document_chain

#MEMORY INISIALIZATION
store = {}
def get_session_history(session_id: str):
    if session_id not in store: store[session_id] = ChatMessageHistory()
    return store[session_id]

#MAKING CHATBOT INVOKABLE FOR FRONTEND
chatbot_with_memory = RunnableWithMessageHistory(
    rag_pipeline, get_session_history, input_messages_key="input", history_messages_key="history"
)