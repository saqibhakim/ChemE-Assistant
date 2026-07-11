from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    base_url="https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY"),
    model="openai/text-embedding-3-small"
)

def ingest_doc(file_path):
 loader = UnstructuredLoader(
    file_path= file_path,
    strategy="fast",
    partition_via_api=True,
    api_key=os.getenv("UNSTRUCTURED_API_KEY"),
    url="https://api.unstructuredapp.io/general/v0/partition" 
)

 docs = loader.load()
 print("="*80)
 print("Loaded docs:", len(docs))

 for i, doc in enumerate(docs[:10]):
    print(doc.metadata)
    print(doc.page_content)
    print("-"*60)

 splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=300
)

 chunks = splitter.split_documents(docs)

 db = FAISS.from_documents(chunks, embeddings)

 DB_PATH = "vectorstore/db_faiss"
 db.save_local(DB_PATH)

 
 return len(chunks)
