import json


class MockClient:
    def generate(self, system: str, user: str) -> str:
        return json.dumps({
            "version": "1.0",
            "goal": "Mock plan",
            "tasks": [
                {
                    "id": "task_1",
                    "type": "tool",
                    "operation": "http_get",
                    "input": {},
                    "depends_on": []
                }
            ]
        })
