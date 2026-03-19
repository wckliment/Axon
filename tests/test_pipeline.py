from app.planner.generate import generate_plan
from app.planner.mock_client import MockClient
from app.executor.engine import execute_plan


def test_end_to_end_mock():
    plan = generate_plan("fetch and summarize data", MockClient())
    result = execute_plan(plan)

    assert result["status"] == "success"
    assert "trace" in result
