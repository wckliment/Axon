from app.planner.schema import ALLOWED_TASK_TYPES, REQUIRED_TOP_LEVEL_FIELDS, REQUIRED_TASK_FIELDS


def validate_plan(plan: dict) -> None:
    if not isinstance(plan, dict):
        raise ValueError("plan must be a dict")

    missing = REQUIRED_TOP_LEVEL_FIELDS - plan.keys()
    if missing:
        raise ValueError(f"plan is missing required fields: {missing}")

    if plan["version"] != "1.0":
        raise ValueError(f"version must be '1.0', got {plan['version']!r}")

    if not isinstance(plan["goal"], str):
        raise ValueError("goal must be a string")

    tasks = plan["tasks"]
    if not isinstance(tasks, list) or len(tasks) == 0:
        raise ValueError("tasks must be a non-empty list")

    seen_ids = set()

    # First pass: validate tasks and collect IDs
    for i, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise ValueError(f"task at index {i} must be a dict")

        missing = REQUIRED_TASK_FIELDS - task.keys()
        if missing:
            raise ValueError(f"task at index {i} is missing required fields: {missing}")

        if not isinstance(task["id"], str) or not task["id"].strip():
            raise ValueError(f"task at index {i}: id must be a non-empty string")

        task_id = task["id"]

        if task["type"] not in ALLOWED_TASK_TYPES:
            raise ValueError(
                f"task {task_id!r}: type must be one of {ALLOWED_TASK_TYPES}, got {task['type']!r}"
            )

        if not isinstance(task["operation"], str):
            raise ValueError(f"task {task_id!r}: operation must be a string")

        if not isinstance(task["input"], dict):
            raise ValueError(f"task {task_id!r}: input must be a dict")

        if not isinstance(task["depends_on"], list):
            raise ValueError(f"task {task_id!r}: depends_on must be a list")

        for dep in task["depends_on"]:
            if not isinstance(dep, str):
                raise ValueError(
                    f"task {task_id!r}: depends_on must contain only strings, got {dep!r}"
                )

        if task_id in seen_ids:
            raise ValueError(f"duplicate task id: {task_id!r}")

        seen_ids.add(task_id)

    # Second pass: validate dependency references
    for task in tasks:
        task_id = task["id"]

        for dep in task["depends_on"]:
            if dep not in seen_ids:
                raise ValueError(
                    f"task {task_id!r}: depends_on references unknown task id {dep!r}"
                )