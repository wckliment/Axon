import re


def score_document(doc: str) -> int:
    # score based on domain-relevant keywords and content length
    score = 0
    text = doc.lower()

    if "embedding" in text:
        score += 3
    if "vector" in text:
        score += 2
    if "search" in text:
        score += 2
    if "model" in text:
        score += 1
    if "semantic" in text:
        score += 2

    # reward longer, meaningful content
    if len(doc) > 120:
        score += 1

    return score


def filter_documents(input_data):
    docs = input_data.get("documents", [])

    if not isinstance(docs, list):
        raise ValueError("filter_documents: documents must be a list")

    # light cleaning only — do not drop content before scoring
    cleaned = []

    for doc in docs:
        if not isinstance(doc, str):
            continue

        # remove HTML tags
        text = re.sub(r"<[^>]+>", "", doc)

        # normalize whitespace
        text = " ".join(text.split())

        cleaned.append(text)

    # score all documents first
    scored = [(doc, score_document(doc)) for doc in cleaned]

    # filter after scoring: drop zero-signal and very short documents
    scored = [(doc, s) for doc, s in scored if s > 0 and len(doc) >= 40]

    # sort by score descending and take top 3
    scored.sort(key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, _ in scored[:3]]

    return {"documents": top_docs}
