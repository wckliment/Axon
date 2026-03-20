from typing import Any, Dict, List

from app.planner.openai_client import OpenAIClient


def summarize_documents(inputs: Dict[str, Any]) -> Dict[str, str]:
    documents = inputs.get("documents")

    if not isinstance(documents, list) or not documents:
        raise ValueError("summarize_documents requires input {'documents': <non-empty list>}")

    docs = [d for d in documents[:5] if isinstance(d, str) and d.strip()]

    if not docs:
        raise ValueError("summarize_documents: no valid document strings found in input")

    combined = "\n\n".join(
        f"Document {i + 1}:\n{doc.strip()}" for i, doc in enumerate(docs)
    )

    client = OpenAIClient()
    summary = client.generate(
        system="You are a technical summarizer for a retrieval system.",
        user=f"""
You are given retrieved document chunks that may contain noise such as HTML, UI artifacts, or broken text.

Your task:
- Produce a clean, readable explanation
- Remove ALL HTML, UI fragments, and broken tokens
- Do NOT repeat raw text
- Do NOT include markup or links
- Rewrite into a coherent explanation

Focus on:
- key concepts
- best practices
- clear explanation

Documents:
{combined}
""",
    )

    # normalize whitespace
    summary = " ".join(summary.split())

    return {"summary": summary}