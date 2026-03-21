import json

from app.planner.validator import validate_plan
from app.planner.prompt import PLANNER_PROMPT


def generate_plan(user_input: str, client) -> dict:
    response_text = client.generate(system=PLANNER_PROMPT, user=user_input)

    try:
        plan = json.loads(response_text)
    except json.JSONDecodeError:
        raise ValueError("invalid JSON from planner")

    validate_plan(plan)

    # Inject the original user query into filter_documents tasks so
    # query-aware scoring has the signal it needs.
    for task in plan.get("tasks", []):
        if task.get("operation") == "filter_documents":
            task["input"].setdefault("query", user_input)

    return plan
