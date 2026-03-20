import re

from app.operations.retrieve_documents import retrieve_documents
from app.operations.summarize_documents import summarize_documents
from app.operations.filter_documents import filter_documents  # ✅ ADDED


def http_get(input_data: object) -> dict:
    return {
        "status": 200,
        "data": {
            "message": "mock response"
        }
    }


def extract_field(input_data: object) -> dict:
    if not isinstance(input_data, dict):
        raise ValueError("extract_field: input must be a dict")

    if "data" not in input_data:
        raise ValueError("extract_field: missing 'data' in input")

    if "path" not in input_data:
        raise ValueError("extract_field: missing 'path' in input")

    data = input_data["data"]
    path = input_data["path"]

    if not isinstance(path, str):
        raise ValueError("extract_field: 'path' must be a string")

    value = data

    for key in path.split("."):
        if not isinstance(value, dict) or key not in value:
            raise ValueError(f"extract_field: invalid path {path!r}")
        value = value[key]

    return {"value": value}


def format_summary(input_data: object) -> dict:
    if not isinstance(input_data, dict):
        raise ValueError("format_summary: input must be a dict")

    if "text" in input_data:
        text = input_data["text"]

    elif "documents" in input_data:
        docs = input_data["documents"]

        if not isinstance(docs, list):
            raise ValueError("format_summary: 'documents' must be a list")

        cleaned_docs = []
        for doc in docs[:3]:
            if not isinstance(doc, str):
                continue

            clean = doc

            # remove HTML tags
            clean = re.sub(r"<[^>]*>", " ", clean)

            # remove URLs
            clean = re.sub(r"http\S+|www\.\S+", " ", clean)

            # remove CMS / JSON artifact fragments
            clean = re.sub(r"(markDefs|style|href|class)[^ ]*", " ", clean)

            # remove escaped characters
            clean = re.sub(r'\\[\"/]', '', clean)

            # remove brackets / braces
            clean = re.sub(r'[\[\]\{\}]+', ' ', clean)

            # remove repeated commas
            clean = re.sub(r'[,]{2,}', ' ', clean)

            # remove stray symbols but keep words + periods
            clean = re.sub(r'[^\w\s\.\-]', ' ', clean)

            # normalize whitespace
            clean = " ".join(clean.split())

            # skip tiny garbage fragments
            if len(clean) < 50:
                continue

            cleaned_docs.append(clean)

        text = ". ".join(cleaned_docs)

        # remove double periods
        text = re.sub(r'\.\s*\.', '.', text)

    else:
        raise ValueError("format_summary: requires 'text' or 'documents'")

    # limit output size
    text = text[:1000]

    return {"summary": text}


OPERATIONS = {
    "http_get": http_get,
    "extract_field": extract_field,
    "format_summary": format_summary,
    "retrieve_documents": retrieve_documents,
    "summarize_documents": summarize_documents,
    "filter_documents": filter_documents,  # ✅ ADDED
}


def execute_operation(operation: str, input_data: object) -> dict:
    if operation not in OPERATIONS:
        raise ValueError(f"Unknown operation: {operation!r}")

    result = OPERATIONS[operation](input_data)

    if not isinstance(result, dict):
        raise ValueError(
            f"Operation {operation!r} must return a dict, got {type(result).__name__}"
        )

    return result