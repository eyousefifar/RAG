from typing import List, Dict, Literal
from app.db import get_database
from bson import ObjectId
import time

db = get_database()


# logger should use an event driven system to write logs of process or in a thread, to avoid blocking
def query_logger(
    history: List[Dict[str, str]],
    query: str,
    context: str,
    answer: str,
    duration: float,
):
    collection = db.get_collection("query_logs")
    collection.insert_one(
        {
            "history": history,
            "query": query,
            "context": context,
            "answer": answer,
            "duration": duration,
            "created_at": time.time(),
        }
    )


def indexing_logger(
    name: str,
    content_str: str,
    type: Literal["file", "text"],
    chunks: List[str],
    duration: float,
):
    collection = db.get_collection("indexing_logs")
    collection.insert_one(
        {
            "name": name,
            "content_str": content_str,
            "type": type,
            "chunks": chunks,
            "duration": duration,
            "created_at": time.time(),
        }
    )


def retrieve_context_logger(query: str, context: str):
    collection = db.get_collection("retrieve_context_logs")
    collection.insert_one(
        {"query": query, "context": context, "created_at": time.time()}
    )
def serialize_document(document):
    """ Convert ObjectId to string in the document. """
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
    return document


def retrieve_logs():
    db = get_database()

    query_logs = db.get_collection("query_logs").find()
    index_logs = db.get_collection("indexing_logs").find()
    context_logs = db.get_collection("retrieve_context_logs").find()

    # Convert cursors to lists and serialize documents
    return {
        "query_logs": [serialize_document(doc) for doc in query_logs],
        "index_logs": [serialize_document(doc) for doc in index_logs],
        "context_logs": [serialize_document(doc) for doc in context_logs]
    }