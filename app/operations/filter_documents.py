import re
from typing import Dict, List, Tuple


def clean_text(text: str) -> str:
    """Strip markup and obvious non-content noise, then normalize whitespace."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[\s*##[^\]]*\]", " ", text)
    text = re.sub(r"(cell_type:|metadata:|source:|outputs:)", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\\[nrt\"'\\]", " ", text)

    if text.count("{") + text.count("}") > 6 or text.count('"') > 10:
        text = re.sub(r"[{}\"]", " ", text)

    text = re.sub(r"^(?:tadata:|=\s*|:\s*source:\s*)+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    text = text.strip("[](){} \t\r\n")
    return text


def compute_fragment_penalty(text: str) -> float:
    """Heuristic penalty for fragmented or noisy chunks. Returns [0, 1]."""
    penalty = 0.0

    if len(text) < 50:
        penalty += 0.5

    if text and text[0].islower():
        penalty += 0.3

    if text and text[-1] not in ".!?":
        penalty += 0.2

    noise_count = text.count("<") + text.count(">")
    if noise_count > 0:
        penalty += min(noise_count * 0.05, 0.3)

    if "return" in text and "=" in text:
        penalty += 0.5

    return min(penalty, 1.0)


def compute_quality_score(text: str) -> float:
    """Heuristic quality score preferring medium-length, clean chunks. Returns [0, 1]."""
    if "cell_type:" in text or "metadata:" in text:
        return 0.1

    if text.count("{") > 3 or text.count("}") > 3:
        return 0.1

    if "def " in text or "return " in text:
        return 0.2

    length = len(text)

    if length < 50:
        score = 0.1
    elif length <= 100:
        score = 0.1 + 0.6 * ((length - 50) / 50)
    elif length <= 800:
        score = 0.7 + 0.3 * ((length - 100) / 700)
    elif length <= 1500:
        score = 1.0 - 0.3 * ((length - 800) / 700)
    else:
        score = 0.3

    newline_count = text.count("\n")
    if newline_count > 10:
        score -= 0.2
    elif newline_count > 5:
        score -= 0.1

    if "```" in text:
        score -= 0.15

    sentence_count = len(re.findall(r"[.!?]+", text))
    if sentence_count >= 2:
        score += 0.1

    if "chunk" in text.lower():
        score += 0.2

    return max(0.0, min(score, 1.0))


def compute_query_score(text: str, query: str) -> float:
    """Fraction of query terms present in text (case-insensitive). Returns [0, 1]."""
    def normalize(word: str) -> str:
        word = word.lower().strip(".,!?")
        if word.endswith("ing"):
            word = word[:-3]
        elif word.endswith("ed"):
            word = word[:-2]
        elif word.endswith("s"):
            word = word[:-1]
        return word

    normalized_text = {
        normalize(word) for word in re.findall(r"\b[a-zA-Z]+\b", text.lower()) if normalize(word)
    }
    query_terms = [normalize(word) for word in re.findall(r"\b[a-zA-Z]+\b", query.lower())]
    query_terms = [word for word in query_terms if len(word) > 3]

    if not query_terms:
        return 0.0

    matches = sum(1 for term in query_terms if term in normalized_text)

    return matches / len(query_terms)


def _keyword_score_normalized(text: str) -> float:
    """Domain keyword score normalized to [0, 1]. Max raw score = 11."""
    text_lower = text.lower()
    raw = 0
    if "embedding" in text_lower:
        raw += 3
    if "vector" in text_lower:
        raw += 2
    if "search" in text_lower:
        raw += 2
    if "model" in text_lower:
        raw += 1
    if "semantic" in text_lower:
        raw += 2
    if len(text) > 120:
        raw += 1
    return min(raw / 11.0, 1.0)


def should_reject_document(raw_text: str, text: str) -> bool:
    """Hard-reject obvious non-explanatory content before scoring."""
    raw_text_lower = raw_text.lower()
    if "<" in raw_text or "href=" in raw_text_lower or "astro-" in raw_text_lower:
        return True

    if text.count(".") < 1:
        return True

    if len(text.split()) < 12:
        return True

    return False


def filter_documents(input_data):
    DEBUG = True
    docs = input_data.get("documents", [])
    query = input_data.get("query", "")
    top_k = input_data.get("top_k", 3)

    if not isinstance(docs, list):
        raise ValueError("filter_documents: documents must be a list")

    results: List[Tuple[str, float, Dict[str, float]]] = []

    for doc in docs:
        if not isinstance(doc, str):
            continue

        text = clean_text(doc)
        if not text.strip():
            continue
        if should_reject_document(doc, text):
            continue

        keyword = _keyword_score_normalized(text)
        query_s = compute_query_score(text, query)
        quality = compute_quality_score(text)
        fragment = compute_fragment_penalty(text)

        final_score = (
            keyword * 0.3
            + query_s * 0.4
            + quality * 0.2
            - fragment * 0.1
        )

        results.append((
            text,
            final_score,
            {
                "keyword": round(keyword, 4),
                "query": round(query_s, 4),
                "quality": round(quality, 4),
                "fragment_penalty": round(fragment, 4),
            },
        ))

    results.sort(key=lambda x: x[1], reverse=True)
    results_full = results.copy()

    # drop very low-signal documents
    results = [r for r in results if r[1] > 0.30]

    if not results:
        results = sorted(results_full, key=lambda r: r[1], reverse=True)[:2]

    if DEBUG and results:
        print("==============================")
        print("FILTER DOCUMENTS OUTPUT (TOP 5)")
        print("==============================")
        print()

        for i, item in enumerate(results[:5], start=1):
            text = item[0] if len(item) > 0 and isinstance(item[0], str) else ""
            score = item[1] if len(item) > 1 else None
            breakdown = item[2] if len(item) > 2 and isinstance(item[2], dict) else {}

            print(f"--- Rank {i} ---")
            print(f"Score: {score}")

            if breakdown:
                print(
                    "Breakdown: "
                    f"keyword={breakdown.get('keyword')}, "
                    f"query={breakdown.get('query')}, "
                    f"quality={breakdown.get('quality')}, "
                    f"fragment_penalty={breakdown.get('fragment_penalty')}"
                )

            print(f"Length: {len(text)}")
            print()
            print("Preview:")
            print(text[:200])
            print()

    results = results[:top_k]

    documents = [text for text, _, _ in results]
    scoring = [
        {"score": round(score, 4), "scoring": breakdown}
        for _, score, breakdown in results
    ]

    return {"documents": documents, "scoring": scoring}
