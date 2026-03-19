def create_trace_entry(
    task_id: str,
    status: str,
    input_data: object,
    output: dict | None,
    error: str | None,
) -> dict:
    return {
        "task_id": task_id,
        "status": status,
        "input": input_data,
        "output": output,
        "error": error,
    }