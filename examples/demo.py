import json

from app.executor.engine import execute_plan

demo_plan = {
    "version": "1.0",
    "goal": "Fetch mock data and produce a formatted summary",
    "tasks": [
        {
            "id": "task_1",
            "type": "tool",
            "operation": "http_get",
            "input": {},
            "depends_on": []
        },
        {
            "id": "task_2",
            "type": "transform",
            "operation": "extract_field",
            "input": {
                "data": {"source": "task_1"},
                "path": "data.message"
            },
            "depends_on": ["task_1"]
        },
        {
            "id": "task_3",
            "type": "transform",
            "operation": "format_summary",
            "input": {
                "text": {"source": "task_2", "path": "value"}
            },
            "depends_on": ["task_2"]
        }
    ]
}

result = execute_plan(demo_plan)
print(json.dumps(result, indent=2))
