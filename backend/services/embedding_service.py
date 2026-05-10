import requests
from core.config import settings

def embed_text(texts: list[str]):

    response = requests.post(
        f"{settings.OPENROUTER_BASE_URL}/embeddings",
        headers={
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "text-embedding-3-small",
            "input": texts   # ✅ pass list instead of single string
        }
    )

    if response.status_code != 200:
        raise Exception(f"Embedding failed: {response.text}")

    data = response.json()["data"]

    # Return list of embeddings in correct order
    return [item["embedding"] for item in data]