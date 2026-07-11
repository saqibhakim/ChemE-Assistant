import os
import streamlit as st
from langchain.messages import HumanMessage, AIMessage
from main import get_retriever, llm, template
from Ingest import ingest_doc
import re

def sanitize_math_delimiters(text: str) -> str:
    """
    Force-converts broken open-source math brackets into 
    standard Streamlit-compliant LaTeX delimiters.
    """
    # 1. Handle block equations: \[ ... \] or [ ... ] containing math
    text = text.replace("\\[", "$$").replace("\\]", "$$")
    
    # 2. Handle inline equations: \( ... \) or ( ... ) containing math
    text = text.replace("\\(", "$").replace("\\)", "$")
    
    # 3. Clean up raw HTML line breaks that open models love to dump
    text = text.replace("<br>", "\n").replace("<br/>", "\n")
    
    return text

# ==================================================
# PAGE
# ==================================================

st.set_page_config(
    page_title="ChemE Assistant",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 ChemE Assistant v1.0")
st.caption("By Saqib Hakim")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "langchain_history" not in st.session_state:
    st.session_state.langchain_history = []

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()

# ==================================================
# DISPLAY CHAT
# ==================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ==================================================
# USER INPUT
# ==================================================

prompt = st.chat_input("Ask something...")

if prompt:

    # ---------- Show user message ----------
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    # ---------- Retrieval ----------
   
    current_retriever = get_retriever()
    
    if current_retriever is None:
        relevant_docs = []
        
    else:
        summary_keywords = [
    "summarize",
    "summary",
    "summarise",
    "overview",
    "paper",
]

        if any(word in prompt.lower() for word in summary_keywords):
         relevant_docs = current_retriever.vectorstore.max_marginal_relevance_search(
         prompt,
         k=30,
         fetch_k=60
)
        else:
         relevant_docs = current_retriever.invoke(prompt)
    context_text = ""

    for i, doc in enumerate(relevant_docs, start=1):
        context_text += (
        f"\n===========================\n"
        f"Retrieved Chunk {i}\n"
        f"Source: {doc.metadata.get('source')}\n\n"
        f"{doc.page_content}\n"
         )

    # ---------- Prompt ----------
    rag_prompt = template.invoke(
        {
            "question": prompt,
            "history": st.session_state.langchain_history,
            "context": context_text
        }
    )

    print("="*80)
    print(context_text)
    print("="*80)

    # ---------- LLM ----------
    raw_response = llm.invoke(rag_prompt.messages).content
    response = sanitize_math_delimiters(raw_response)

    # ---------- Show assistant ----------
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    with st.chat_message("assistant"):
        st.write(response)

    # ---------- LangChain History ----------
    st.session_state.langchain_history.append(
        HumanMessage(content=prompt)
    )

    st.session_state.langchain_history.append(
        AIMessage(content=response)
    )

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("📚 Knowledge Base")

    files = st.file_uploader(
        "Upload documents",
        accept_multiple_files=True
    )

    if files:

        for file in files:

            if file.name in st.session_state.indexed_files:
                continue

            filepath = os.path.join(
                UPLOAD_DIR,
                file.name
            )

            with open(filepath, "wb") as f:
                f.write(file.getbuffer())

            st.success(f"Uploaded: {file.name}")

            with st.spinner("Indexing document..."):
                num_chunks = ingest_doc(filepath)

            st.success(f"Indexed {num_chunks} chunks.")
            st.session_state.indexed_files.add(file.name)
            
            # FORCE STREAMLIT TO RERUN SO THE NEW VECTOR STORE IS LOADED
            st.rerun()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []
        st.session_state.langchain_history = []
        st.session_state.indexed_files = set() # Keep it a set as initialized

        st.rerun()