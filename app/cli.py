import sys
import json

from app.planner.generate import generate_plan
from app.planner.openai_client import OpenAIClient
from app.executor.engine import execute_plan

user_input = " ".join(sys.argv[1:])

if not user_input:
    raise ValueError("No input provided")

plan = generate_plan(user_input, OpenAIClient())
result = execute_plan(plan)

print(json.dumps({
    "plan": plan,
    "result": result
}, indent=2))
