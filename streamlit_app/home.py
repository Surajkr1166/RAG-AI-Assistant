"""
Home page for Streamlit chat interface.
"""
import uuid
import streamlit as st
from utils.api_client import query_backend, document_upload_rag

st.set_page_config(
    page_title="IntelliSearch",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 IntelliSearch - Adaptive RAG Chatbot")
st.markdown("Upload documents and ask questions!")

# Initialize session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar - Document Upload
with st.sidebar:
    st.header("📂 Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"]
    )
    if uploaded_file:
        file_description = st.text_input(
            "Describe your document",
            placeholder="E.g. Python tutorial document"
        )
        if file_description:
            if st.button("Upload"):
                with st.spinner("Uploading..."):
                    success = document_upload_rag(
                        uploaded_file,
                        file_description
                    )
                    if success:
                        st.success("Document uploaded!")
                    else:
                        st.error("Upload failed!")

# Chat Interface
user_input = st.chat_input("Ask a question...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Thinking..."):
        response = query_backend(
            user_input,
            st.session_state.session_id
        )
    st.session_state.chat_history.append(("assistant", response))
    st.rerun()

for role, text in st.session_state.chat_history:
    st.chat_message(role).write(text)