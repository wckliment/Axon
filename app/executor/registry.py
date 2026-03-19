def http_get(input: dict) -> dict:
    return {
        "status": 200,
        "data": {
            "message": "mock response"
        }
    }


def extract_field(input: dict) -> dict:
    if not isinstance(input, dict):
        raise ValueError("extract_field: input must be a dict")

    if "data" not in input:
        raise ValueError("extract_field: missing 'data' in input")

    if "path" not in input:
        raise ValueError("extract_field: missing 'path' in input")

    data = input["data"]
    path = input["path"]

    if not isinstance(path, str):
        raise ValueError("extract_field: 'path' must be a string")

    value = data

    for key in path.split("."):
        if not isinstance(value, dict) or key not in value:
            raise ValueError(f"extract_field: invalid path {path!r}")
        value = value[key]

    return {"value": value}


def format_summary(input: dict) -> dict:
    if not isinstance(input, dict):
        raise ValueError("format_summary: input must be a dict")

    if "text" not in input:
        raise ValueError("format_summary: missing 'text' in input")

    text = input["text"]

    return {"summary": f"Summary: {text}"}


OPERATIONS = {
    "http_get": http_get,
    "extract_field": extract_field,
    "format_summary": format_summary,
}


def execute_operation(operation: str, input: dict) -> dict:
    if operation not in OPERATIONS:
        raise ValueError(f"Unknown operation: {operation!r}")

    result = OPERATIONS[operation](input)

    if not isinstance(result, dict):
        raise ValueError(
            f"Operation {operation!r} must return a dict, got {type(result).__name__}"
        )

    return result