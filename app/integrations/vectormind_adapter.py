import re
from typing import Dict, List, Tuple

from vectormind.retrieve import retrieve


def _normalize_chunk(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^(?:tadata:|metadata:|cell_type:|source:|outputs:|=\s*|:\s*source:\s*)+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()

    complete_sentences = re.findall(r"(?:^|(?<=[.!?]\s))([A-Z0-9][^.!?]*[.!?])", text)
    if complete_sentences:
        return " ".join(sentence.strip() for sentence in complete_sentences)

    return text


def retrieve_documents_from_vectormind(query: str, k: int = 10) -> Tuple[List[str], List[Dict]]:
    result = retrieve(query, k=k)

    documents = result.get("documents", [])
    if not documents:
        return [], []

    docs = documents[0]
    metadatas = (result.get("metadatas") or [[]])[0]
    distances = (result.get("distances") or [[]])[0]

    print("VECTORMIND RAW RETRIEVED CHUNKS:")
    for index, doc in enumerate(docs, start=1):
        print(f"[{index}] {doc}")

    cleaned = []
    raw_chunks = []
    for i, doc in enumerate(docs):
        if isinstance(doc, str):
            text = _normalize_chunk(doc)
            if text:
                cleaned.append(text)

        meta = metadatas[i] if i < len(metadatas) else {}
        raw_chunks.append({
            "score": distances[i] if i < len(distances) else None,
            "metadata": meta if isinstance(meta, dict) else {},
            "text": doc if isinstance(doc, str) else None,
        })

    return cleaned, raw_chunks
