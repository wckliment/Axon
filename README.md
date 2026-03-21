# Axon

> Deterministic AI execution engine.
> LLM plans. Runtime executes. Every step is validated and traceable.

Axon is a deterministic LLM orchestration engine that turns model-generated plans into controlled, executable workflows.

Built as part of a series of AI systems focused on production reliability, orchestration, and retrieval.

It separates **planning (LLM)** from **execution (runtime)** to make AI workflows reliable, debuggable, and production-ready.

This project demonstrates how to build production-grade AI systems that remain reliable under real-world conditions.

---

## Overview

Most LLM systems rely on prompt chaining and implicit behavior. This makes them difficult to debug, validate, and trust in production.

Axon enforces a different model:

* LLMs generate **structured plans**
* The runtime **controls execution**
* Every step is **validated and traceable**

This creates a system that is predictable under real-world conditions—external APIs, multi-step workflows, and unreliable inputs.

---

## Architecture

```
+-------------+      +-----------------+      +----------------------+
| User Input  | ---> | LLM Planner     | ---> | JSON Task Plan       |
+-------------+      +-----------------+      +----------------------+
                                                      |
                                                      v
                                        +---------------------------+
                                        | Deterministic Executor    |
                                        | - task queue              |
                                        | - dependency handling     |
                                        | - state management        |
                                        +---------------------------+
                                              |              |
                                              v              v
                                  +------------------+   +------------------+
                                  | Tool Layer       |   | Validation Layer |
                                  | - retrieval      |   | - schema checks  |
                                  | - API calls      |   | - retries        |
                                  +------------------+   +------------------+
                                              \              /
                                               \            /
                                                v          v
                                          +----------------------+
                                          | Execution Trace      |
                                          | - step history       |
                                          | - inputs / outputs   |
                                          | - UI inspector       |
                                          +----------------------+
```

---

## Demo

![Axon Execution Trace](./docs/demo.gif)

* Step-by-step execution trace
* JSON input/output inspection
* Error visibility and retry behavior
* This makes it possible to debug and understand AI behavior at a system level instead of relying on opaque model outputs.

---

## Execution Model

1. User submits a request
2. LLM generates a structured JSON task plan
3. Executor processes tasks deterministically
4. Tools are invoked explicitly (retrieval / APIs)
5. Outputs are validated before proceeding
6. Full execution trace is recorded

---

## Features

* Structured JSON planning (no free-form execution)
* Deterministic task execution engine
* Tool integration (retrieval + external APIs)
* Validation layer with retry handling
* Full execution trace with step inspection
* Clear separation of planning vs execution
* UI for inspecting execution traces and step-level behavior

---

## Example Flow

### Input

```
Summarize recent customer issues and identify the top 3 recurring problems
```

### Plan

```json
{
  "tasks": [
    {
      "id": "fetch_tickets",
      "type": "retrieval",
      "input": {
        "source": "support_tickets",
        "query": "recent customer issues"
      }
    },
    {
      "id": "group_issues",
      "type": "llm_transform",
      "input": {
        "from": "fetch_tickets",
        "instruction": "Cluster similar issues and count frequency"
      }
    },
    {
      "id": "rank_top_issues",
      "type": "sort",
      "input": {
        "from": "group_issues",
        "by": "frequency",
        "limit": 3
      }
    }
  ]
}
```

### Execution

* Retrieve support tickets
* Cluster and count issue categories
* Rank top 3 issues
* Validate output
* Record full trace

---

## Use Cases

* Multi-step AI workflows with tool usage
* Retrieval + reasoning pipelines
* API orchestration with LLM planning
* Systems that require traceability, validation, and control over AI behavior

---

## Tech Stack

* **Backend:** Python, FastAPI
* **Frontend:** React
* **Planning Layer:** LLM APIs
* **Retrieval:** vector search / embeddings
* **Runtime:** deterministic task executor

---

## Project Structure

```
axon/
├── backend/
│   ├── api/           # Entry point (POST /run)
│   ├── planner/       # LLM planning logic
│   ├── runtime/       # Execution engine
│   ├── tools/         # Retrieval + API tools
│   ├── validation/    # Output validation
│   └── tracing/       # Execution logs
├── frontend/
│   ├── components/    # Trace UI + inspector
│   └── App.tsx
├── docs/
├── tests/
└── README.md
```

---

## Getting Started

### Prerequisites

* Python 3.11+
* Node.js 18+
* LLM API access
* Vector retrieval backend

### Setup

```bash
git clone https://github.com/<your-org>/axon.git
cd axon
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn api.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Design Principles

* **The model proposes, the system decides**
  LLMs generate intent. The runtime controls execution.

* **Deterministic > prompt chaining**
  Explicit task execution is more reliable than hidden prompt loops.

* **Observable > opaque**
  Every step is logged, inspectable, and debuggable.

* **Structured > free-form**
  Plans are machine-checkable before execution begins.

---

## Why This Matters

LLMs are powerful for generating intent, but unreliable as execution environments.

Most systems:

* hide execution inside prompts
* lack validation boundaries
* are difficult to debug

Axon treats the LLM as a **planner**, not an autonomous system.

This enables:

* reliable multi-step workflows
* safe tool usage
* full traceability of behavior

This is the difference between a demo and a production system.

---

## Future Improvements

* Parallel task execution with dependency graphs
* Stronger typed schemas and versioning
* Dynamic tool registry
* Advanced retry and recovery strategies
* Evaluation pipelines for plan quality
* Persistent memory layer

---

## License

MIT License
