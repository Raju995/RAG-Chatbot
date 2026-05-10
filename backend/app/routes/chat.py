from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import ChatHistory
from services.retrieval_service import retrieve_similar_chunks
from services.prompt_service import build_chat_prompt
from services.llm_service import generate_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    session_id: str


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat endpoint that prevents hallucinations by:
    1. Checking for relevant context before answering
    2. Using proper prompt structure
    3. Handling low-confidence scenarios
    """
    # 1️⃣ Retrieve similar chunks with relevance check
    similar_chunks = retrieve_similar_chunks(request.question, db)
    
    # 2️⃣ CRITICAL: Check if we have relevant context
    if not similar_chunks:
        # Save to history
        db.add(ChatHistory(
            session_id=request.session_id,
            role="user",
            message=request.question
        ))
        fallback_response = "I cannot answer this question based on the provided document. The information is not present in the text."
        db.add(ChatHistory(
            session_id=request.session_id,
            role="assistant",
            message=fallback_response
        ))
        db.commit()
        return {"response": fallback_response}
    
    # 3️⃣ Continue with normal flow if relevant context exists
    context = "\n\n".join([chunk["content"] for chunk in similar_chunks])
    
    # 4️⃣ Load chat history
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == request.session_id)
        .order_by(ChatHistory.id.asc())
        .limit(5)
        .all()
    )
    
    # 5️⃣ Build prompt with STRICT instructions
    messages = build_chat_prompt(
        question=request.question,
        context=context,
        history=history
    )
    
    # 6️⃣ Generate answer
    answer = generate_answer(messages)

    # 7️⃣ Save history
    db.add(ChatHistory(
        session_id=request.session_id,
        role="user",
        message=request.question
    ))

    db.add(ChatHistory(
        session_id=request.session_id,
        role="assistant",
        message=answer
    ))

    db.commit()

    return {"response": answer}