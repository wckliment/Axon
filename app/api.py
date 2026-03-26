from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.planner.generate import generate_plan
from app.planner.openai_client import OpenAIClient
from app.executor.engine import execute_plan


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    input: str


@app.post("/run")
def run_pipeline(request: RunRequest):
    plan = generate_plan(request.input, OpenAIClient())
    execution = execute_plan(plan, user_input=request.input)

    retrieval_debug = execution.get("retrieval_debug") or {
        "query": request.input,
        "top_k": [],
    }

    return {
        "plan": plan,
        "trace": execution.get("trace"),
        "result": execution.get("result"),
        "retrieval_debug": retrieval_debug,
    }