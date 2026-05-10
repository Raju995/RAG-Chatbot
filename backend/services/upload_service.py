import os
import json
from uuid import uuid4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from app.models import  DocumentChunk,Document
from services.embedding_service import embed_text


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def process_pdf(file, db):

    # 1️⃣ Save file
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # 2️⃣ Store document metadata
    document = Document(doc_name=file.filename)
    db.add(document)
    db.commit()
    db.refresh(document)

    # 3️⃣ Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 4️⃣ Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    texts = text_splitter.split_documents(docs)

    chunk_texts = [doc.page_content for doc in texts]

    # 1️⃣ Batch embed (ONE API CALL internally)
    embeddings = embed_text(chunk_texts)   # returns list of vectors

    # 2️⃣ Store all chunks
    for doc, embedding in zip(texts, embeddings):
        chunk = DocumentChunk(
            doc_id=doc.metadata.get("doc_id"),  # or however you're storing doc id
            content=doc.page_content,
            embedding=json.dumps(embedding)
        )

        db.add(chunk)

    db.commit()

    return {"message": "PDF processed successfully"}