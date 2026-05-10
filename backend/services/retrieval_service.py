import json
import numpy as np
from app.models import DocumentChunk
from services.embedding_service import embed_text


def cosine_similarity(a, b):
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_similar_chunks(question: str, db, top_k=3, relevance_threshold=0.3):
    """
    Retrieve chunks with relevance threshold to prevent hallucinations
    
    Args:
        question: User question
        db: Database session
        top_k: Maximum number of chunks to return
        relevance_threshold: Minimum similarity score to consider a chunk relevant
    
    Returns:
        List of relevant chunks with content and score
    """
    question_embedding = embed_text([question])
    question_embedding = [float(x) for x in question_embedding[0]]

    chunks = db.query(DocumentChunk).all()
    similarities = []

    for chunk in chunks:
        stored_embedding = json.loads(chunk.embedding)
        stored_embedding = [float(x) for x in stored_embedding]

        score = cosine_similarity(question_embedding, stored_embedding)
        similarities.append({
            "content": chunk.content,
            "score": score
        })

    # Sort by score and filter by relevance threshold
    similarities = sorted(similarities, key=lambda x: x["score"], reverse=True)
    relevant_chunks = [chunk for chunk in similarities if chunk["score"] >= relevance_threshold]

    return relevant_chunks[:top_k]
