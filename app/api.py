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
    result = execute_plan(plan)

    return {
        "plan": plan,
        "result": result,
    }