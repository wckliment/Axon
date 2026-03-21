from typing import Any, Dict, List

from app.integrations.vectormind_adapter import retrieve_documents_from_vectormind


def retrieve_documents(inputs: Dict[str, Any]) -> Dict[str, List[str]]:
    query = inputs.get("query")

    if not isinstance(query, str) or not query.strip():
        raise ValueError("retrieve_documents requires input {'query': <non-empty string>}")

    documents = retrieve_documents_from_vectormind(query.strip(), k=10)

    return {"documents": documents}
