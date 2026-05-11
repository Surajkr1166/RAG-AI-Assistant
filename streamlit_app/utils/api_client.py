"""
API client for communicating with backend services.
"""
import requests

PYTHON_BASE_URL = "http://127.0.0.1:8000"


def query_backend(query: str, session_id: str) -> str:
    """
    Send a query to the RAG backend.
    """
    url = f"{PYTHON_BASE_URL}/rag/query"
    try:
        response = requests.post(
            url,
            json={"query": query, "session_id": session_id},
        )
        if response.status_code == 200:
            return response.json()["result"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection error: {str(e)}"


def document_upload_rag(file, description: str) -> bool:
    """
    Upload a document to the RAG system.
    """
    headers = {"X-Description": description}
    url = f"{PYTHON_BASE_URL}/rag/documents/upload"

    if file:
        files = {"file": (file.name, file, file.type)}
        try:
            response = requests.post(url, files=files, headers=headers)
            if response.status_code == 200:
                return True
        except Exception as e:
            print(f"Upload error: {e}")

    return False