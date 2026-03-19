import json

from app.executor.engine import execute_plan

demo_plan = {
    "version": "1.0",
    "goal": "Demonstrate execution failure",
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
                "path": "data.invalid_field"
            },
            "depends_on": ["task_1"]
        }
    ]
}

result = execute_plan(demo_plan)
print(json.dumps(result, indent=2))
