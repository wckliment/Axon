from app.planner.validator import validate_plan
from app.executor.resolver import resolve_input
from app.executor.registry import execute_operation
from app.executor.trace import create_trace_entry


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