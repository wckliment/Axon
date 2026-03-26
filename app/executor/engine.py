from app.planner.validator import validate_plan
from app.executor.resolver import resolve_input
from app.executor.registry import execute_operation
from app.executor.trace import create_trace_entry
from vectormind.answer import answer_question


def _documents_are_relevant(documents: list, query: str) -> bool:
    """Strict relevance check based on keyword overlap."""
    if not documents:
        return False

    query_terms = {w.lower() for w in query.split() if len(w) > 3}
    if not query_terms:
        return False

    combined = " ".join(documents).lower()

    overlap = sum(1 for term in query_terms if term in combined)

    # Require at least one meaningful overlap
    return overlap >= 1


def execute_plan(plan: dict, user_input: str = "") -> dict:
    validate_plan(plan)

    results = {}
    trace = []
    last_output = None
    retrieval_debug = None

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

            if isinstance(output, dict) and "retrieval_debug" in output:
                retrieval_debug = output["retrieval_debug"]

            results[task_id] = output
            last_output = output

            trace.append(
                create_trace_entry(task_id, "success", resolved_input, output, None)
            )

            if isinstance(output, dict) and "documents" in output:
                result = answer_question(user_input)
                print("AXON RECEIVED ANSWER:", result["result"])
                return {
                    "status": "success",
                    "result": result["result"],
                    "trace": trace,
                    "retrieval_debug": result.get("retrieval_debug") or retrieval_debug,
                }

        except Exception as e:
            trace.append(
                create_trace_entry(task_id, "failed", resolved_input, None, str(e))
            )
            return {
                "status": "failed",
                "result": None,
                "trace": trace,
                "retrieval_debug": retrieval_debug,
            }

    return {
        "status": "success",
        "result": last_output,
        "trace": trace,
        "retrieval_debug": retrieval_debug,
    }