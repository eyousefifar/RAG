# NOTE: using chroma db for simplicity, I would consider Qdrant for production
# because of it's effective implementation of BM25, Colbert and ColPoli ( PDFs files for example, in this case I recommend pre-processing )
import chromadb


# Docling offers good tools, also available in llama index
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.base_models import DocumentStream
from io import BytesIO
import time
import uuid
from chonkie import SemanticChunker

from .logging import indexing_logger, retrieve_context_logger

# leaving this here in favor of Qdrant
try:
    client = chromadb.PersistentClient()

    collection = client.get_or_create_collection("documents")
except Exception as e:
    raise e


def _process_file(name: str, file: bytes):
    try:
        converter = DocumentConverter(
            allowed_formats=[
                InputFormat.XLSX,
                InputFormat.PDF,
                InputFormat.DOCX,
                InputFormat.IMAGE,
                InputFormat.MD,
                InputFormat.PPTX,
            ]
        )
        file_stream = BytesIO(file)
        d_st = DocumentStream(name=name, stream=file_stream)
        result = converter.convert(source=d_st)
        markdown = result.document.export_to_markdown()
        return markdown
        # maybe this can be faster

    except Exception as e:
        raise e


def index_document(
    name: str,
    data: bytes | str,
) -> bool:
    startTime = time.time()
    content = data
    print(isinstance(data, bytes))
    if isinstance(data, bytes):
        content = _process_file(name, data)
    # Chunking is the key to RAG effectiveness, I'll Explain this in ReadMe
    chunker = SemanticChunker(
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        threshold=0.7,
        chunk_size=64,
        min_sentences=1,
    )
    chunks = chunker.chunk(content)
    # maybe can be faster if needed
    for chunk in chunks:
        collection.add(documents=[chunk.text], ids=[str(uuid.uuid4())])


    endTime = time.time()
    indexing_logger(
        name=name,
        content_str=content,
        type="file" if isinstance(data, bytes) else "text",
        chunks=[ch.text for ch in chunks],
        duration=endTime - startTime,
    )
    return True


def retrieve_context(query: str) -> str:
    try:
        results = collection.query(
            query_texts=[query],
            n_results=5,
        )
        contexts = results["documents"][0]
        context = "\n".join(contexts)

        retrieve_context_logger(query=query, context=context)
        return context
    except Exception as e:
        print(e)
        return "Error retrieving context"
