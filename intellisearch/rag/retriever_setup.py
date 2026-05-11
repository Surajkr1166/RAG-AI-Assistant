"""
Retriever setup and vector store configuration.
"""
import os
from langchain_core.documents import Document
from langchain_core.tools import create_retriever_tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

_faiss_vectorstore = None


def retriever_chain(chunks: list[Document]):
    """
    Initialize and store documents in FAISS vector database.
    """
    global _faiss_vectorstore
    try:
        vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )
        _faiss_vectorstore = vectorstore
        print("FAISS vector store initialized with documents")
        return True
    except Exception as e:
        print(f"Error storing documents in FAISS: {e}")
        return False


def get_retriever():
    """
    Get a retriever tool connected to the FAISS vector store.
    """
    global _faiss_vectorstore
    try:
        if _faiss_vectorstore is not None:
            retriever = _faiss_vectorstore.as_retriever()
        else:
            dummy_doc = Document(
                page_content="No documents uploaded yet. Please upload a document first.",
                metadata={"source": "initialization"}
            )
            _faiss_vectorstore = FAISS.from_documents(
                documents=[dummy_doc],
                embedding=embeddings
            )
            retriever = _faiss_vectorstore.as_retriever()

        if os.path.exists("description.txt"):
            with open("description.txt", "r", encoding="utf-8") as f:
                description = f.read()
        else:
            description = "uploaded documents"

        retriever_tool = create_retriever_tool(
            retriever,
            "retriever_customer_uploaded_documents",
            f"Use this tool only to answer questions about: {description}\n"
            "Don't use this tool to answer anything else."
        )
        return retriever_tool

    except Exception as e:
        print(f"Error initializing retriever: {e}")
        raise Exception(e)