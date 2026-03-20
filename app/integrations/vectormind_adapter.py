from typing import List

from vectormind.retrieve import retrieve


def retrieve_documents_from_vectormind(query: str, k: int = 5) -> List[str]:
    result = retrieve(query, k=k)

    documents = result.get("documents", [])
    if not documents:
        return []

    docs = documents[0]

    cleaned = []
    for doc in docs:
        if isinstance(doc, str):
            text = doc.strip()
            if text:
                cleaned.append(text)

    return cleaned