from app.planner.validator import validate_plan
from app.executor.resolver import resolve_input
from app.executor.registry import execute_operation
from app.executor.trace import create_trace_entry


def _documents_are_relevant(documents: list, query: str) -> bool:
    """Return True if any document shares at least one meaningful keyword with the query."""
    keywords = {w.lower() for w in query.split() if len(w) > 3}
    if not keywords:
        return True  # can't determine irrelevance without keywords, don't block
    combined = " ".join(documents).lower()
    return any(kw in combined for kw in keywords)


def execute_plan(plan: dict) -> dict:
    validate_plan(plan)

    results = {}
    trace = []
    last_output = None

    for task in plan["tasks"]:
        task_id = task["id"]
        resolved_input = None

        try:
            for dep in task["depends_on"]:
                if dep not in results:
                    raise ValueError(
                        f"task {task_id!r}: dependency {dep!r} has not been executed"
                    )

            resolved_input = resolve_input(task["input"], results)
            output = execute_operation(task["operation"], resolved_input)

            results[task_id] = output
            last_output = output

            trace.append(
                create_trace_entry(task_id, "success", resolved_input, output, None)
            )

            # Guard: stop before generation if retrieval failed or returned irrelevant documents
            if isinstance(output, dict) and "documents" in output:
                docs = output["documents"]
                query = resolved_input.get("query", "") if isinstance(resolved_input, dict) else ""
                if not docs or not _documents_are_relevant(docs, query):
                    return {
                        "status": "success",
                        "result": "I don't know based on available information.",
                        "trace": trace,
                    }

        except Exception as e:
            trace.append(
                create_trace_entry(task_id, "failed", resolved_input, None, str(e))
            )
            return {
                "status": "failed",
                "result": None,
                "trace": trace,
            }

    return {
        "status": "success",
        "result": last_output,
        "trace": trace,
    }