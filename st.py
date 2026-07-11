import streamlit as st
st.title("ChemE Assistant v1.0")
st.write("By Saqib Hakim")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages: 
    with st.chat_message(msg["role"]): 
        st.write(msg["content"])



prompt = st.chat_input("Ask something")

if prompt:
    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    response = "naacho"

    st.session_state.messages.append(
        {"role":"assistant","content":response}
    )

    with st.chat_message("assistant"):
        st.write(response)

    


with st.sidebar:

    st.header("Knowledge Base")
    files = st.file_uploader(
        "Add documents",
        accept_multiple_files=True
    )

    if files:
     for file in files:
        st.write(file.name)
        st.write(file.type)
        st.write(file.size)
    

    if st.button("Clear Chat"):
        st.session_state.messages = []
    
   