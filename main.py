"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from intellisearch.api.routes import router

app = FastAPI(title="IntelliSearch - Adaptive RAG API")
app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {"message": "IntelliSearch Adaptive RAG API is running!"}