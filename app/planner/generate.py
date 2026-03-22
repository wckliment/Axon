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

    # Inject the original user query into retrieval and filter tasks.
    # For retrieve_documents, override the query entirely — the full user
    # input produces better vector matches than the short keyword the LLM picks.
    # For filter_documents, only set if missing (scoring may already have it).
    for task in plan.get("tasks", []):
        if task.get("operation") == "retrieve_documents":
            task["input"]["query"] = user_input
        elif task.get("operation") == "filter_documents":
            task["input"].setdefault("query", user_input)

    return plan
