def build_chat_prompt(question: str, context: str, history: list):

    # ---------------------------
    # Format chat history
    # ---------------------------
    formatted_history = []

    for msg in history:
        role = "user" if msg.role == "user" else "assistant"
        formatted_history.append({
            "role": role,
            "content": msg.message
        })

    # ---------------------------
    # System Instructions
    # ---------------------------
    system_message = {
        "role": "system",
        "content": """
You are a professional AI assistant specialized in answering questions 
from provided PDF documents.

STRICT RULES:
- Use ONLY the provided document context.
- If answer is not present, say: "Answer not found in document."
- Do NOT make up information.
- Keep answers concise and accurate.
- If follow-up question is unclear, use conversation history to infer meaning.
"""
    }

    # ---------------------------
    # Context Injection
    # ---------------------------
    context_message = {
        "role": "system",
        "content": f"""
        DOCUMENT CONTEXT:
        {context}
        """
    }

    # ---------------------------
    # Current User Question
    # ---------------------------
    user_message = {
        "role": "user",
        "content": question
    }

    # ---------------------------
    # Final Message List
    # ---------------------------
    messages = [system_message]

    # Add history
    messages.extend(formatted_history)

    # Add context
    messages.append(context_message)

    # Add current question
    messages.append(user_message)

    return messages