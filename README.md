# Axon — Deterministic Task Orchestration Engine

LLM-generated plans executed deterministically with validation and full traceability.

---

## What It Does

Axon takes a structured JSON plan produced by an LLM and executes it step-by-step using a deterministic engine. Each task's inputs are resolved from the outputs of prior tasks, every step is validated before and during execution, and the full execution trace is returned with the result. The LLM is involved only in plan generation — it has no influence over execution.

---

## Why

LLM-based systems are often non-deterministic, difficult to debug, and tightly coupled to model behavior.

Axon isolates the LLM to a single responsibility — plan generation — and enforces deterministic execution through a strict runtime. This makes task workflows predictable, testable, and observable.

---

## Core Concepts

- **Planner (LLM)** — generates a structured JSON plan (not executed directly)
- **Validator** — enforces schema correctness before any execution begins
- **Executor** — runs tasks sequentially in declaration order
- **Resolver** — resolves task inputs by injecting outputs from upstream tasks
- **Operation Registry** — maps operation names to callable tool and transform functions
- **Execution Trace** — captures input, output, and status for every task

---

## Example

**Flow:**

```
User request → LLM generates plan → validate_plan() → execute_plan() → result + trace
```

**Single task:**

```json
{
  "id": "task_2",
  "type": "transform",
  "operation": "extract_field",
  "input": {
    "data": { "source": "task_1" },
    "path": "data.message"
  },
  "depends_on": ["task_1"]
}
```

The `source` key tells the resolver to inject the output of `task_1` at runtime.

---

## Running the Demo

```bash
python -m examples.demo
python -m examples.demo_failure
```

Or via CLI:

```bash
axon "Get a message and summarize it"
```

- `demo` — executes a three-task plan end-to-end and prints the full result
- `demo_failure` — executes a plan where a task references an invalid path, producing a controlled failure with a partial trace

---

## Example Output

```json
{
  "status": "success",
  "result": {
    "summary": "Summary: mock response"
  },
  "trace": [
    { "task_id": "task_1", "status": "success" },
    { "task_id": "task_2", "status": "success" }
  ]
}
```

---

## Design Principles

- **Deterministic execution** — the LLM does not participate in the control loop
- **Fail-fast validation** — schema errors are caught before execution begins
- **No hidden state** — all data flow between tasks is explicit via the resolver
- **Explicit data flow** — task inputs declare their sources; nothing is implicit
- **Full observability** — every step produces a trace entry regardless of outcome
- **Controlled execution boundary** — LLM output is treated as untrusted input and strictly validated before execution
---

## Scope

**This is not:**
- a chatbot or conversational agent  
- a full agent framework  
- production infrastructure  
- an autonomous agent system (no LLM control loop)  

**This is:**
- a minimal orchestration core
- a demonstration of reliability patterns for LLM-driven task execution

---

## Future Extensions

- Parallel execution for independent tasks
- Real API integrations in the operation registry
- Persistent execution logs
