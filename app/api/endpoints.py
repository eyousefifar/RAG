from fastapi import APIRouter, UploadFile, HTTPException
from app.services import (
    index_document,
    retrieve_context,
    generate_answer,
    retrieve_logs,
)
from pydantic import BaseModel

from typing import List, TypedDict


class Message(TypedDict):
    role: str
    content: str


class IndexText(BaseModel):
    name: str
    text: str


router = APIRouter()


@router.post("/index-doc")
async def index_doc(name: str, file: UploadFile | None = None):
    try:  # should validate file type
        if not file:
            raise HTTPException(status_code=400, detail="upload a file!")
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="File is empty.")
        success = index_document(name, content)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to index document.")
        return {"message": "Document indexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/index-text")
async def index_text(info: IndexText):
    try:
        success = index_document(info.name, info.text)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to index document.")
        return {"message": "Document indexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class Query(BaseModel):
    query: str
    history: List[Message]


@router.post("/query")
async def query_answering(info: Query):
    """Answer a question using the indexed documents."""
    try:
        context = retrieve_context(info.query)
        answer = generate_answer(info.query, context, info.history)
        return {"question": info.query, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs")
async def get_logs():
    """Fetch logs of queries and responses."""
    try:
        return retrieve_logs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    return {"message": "API is running", "status": "healthy"}
