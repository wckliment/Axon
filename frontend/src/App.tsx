import { useState, useEffect } from "react";

type Task = {
  id: string;
  operation: string;
};

type TraceStep = {
  task_id: string;
  status: "success" | "failed";
  input: unknown;
  output: unknown | null;
  error: string | null;
};

type ApiResponse = {
  plan: {
    tasks: Task[];
  };
  result: {
    result: unknown;
    trace: TraceStep[];
  };
};

export default function App() {
  const [input, setInput] = useState("");
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [visibleSteps, setVisibleSteps] = useState<TraceStep[]>([]);
  const [selectedStep, setSelectedStep] = useState<TraceStep | null>(null);

  useEffect(() => {
    if (!data) return;
    setVisibleSteps([]);
    data.result.trace.forEach((step, i) => {
      setTimeout(() => {
        setVisibleSteps((prev) => [...prev, step]);
      }, i * 400);
    });
  }, [data]);

  const run = async () => {
    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ input }),
    });

    const json: ApiResponse = await res.json();
    setData(json);
    setLoading(false);
  };

  return (
    <>
    <style>{`@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }`}</style>
    <div
      style={{
        background: "#0f172a",
        color: "#e5e7eb",
        minHeight: "100vh",
        padding: "40px 24px",
        fontFamily: "monospace",
      }}
    >
      <div style={{ maxWidth: 900, margin: "0 auto" }}>

        {/* HEADER */}
        <div style={{ marginBottom: 30 }}>
          <h1 style={{ margin: 0, fontSize: 28, color: "#e5e7eb" }}>Axon</h1>
          <p style={{ margin: "6px 0 0", color: "#94a3b8", fontSize: 14 }}>
            Deterministic Task Execution Engine
          </p>
        </div>

        {/* INPUT */}
        <div style={{ marginBottom: 30 }}>
          <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
            <textarea
              rows={3}
              style={{
                flex: 1,
                background: "#020617",
                color: "#e5e7eb",
                border: "1px solid #334155",
                borderRadius: 6,
                padding: 10,
                fontSize: 14,
                resize: "vertical",
              }}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter a task..."
            />
            <button
              onClick={run}
              disabled={loading}
              style={{
                background: "#6366f1",
                color: "#ffffff",
                border: "none",
                borderRadius: 6,
                padding: "10px 20px",
                fontSize: 14,
                cursor: loading ? "not-allowed" : "pointer",
                opacity: loading ? 0.7 : 1,
                whiteSpace: "nowrap",
              }}
            >
              {loading ? "Running..." : "Run"}
            </button>
          </div>
        </div>

        {data && (
          <>
            {/* PLAN */}
            <section style={{ marginBottom: 30 }}>
              <h2 style={{ margin: "0 0 12px", fontSize: 16, color: "#e5e7eb" }}>Plan</h2>
              {data.plan.tasks.map((task) => (
                <div
                  key={task.id}
                  style={{
                    background: "#020617",
                    border: "1px solid #334155",
                    borderRadius: 6,
                    padding: 10,
                    marginBottom: 8,
                    fontSize: 14,
                  }}
                >
                  <strong style={{ color: "#e5e7eb" }}>{task.id}</strong>
                  <span style={{ color: "#94a3b8", marginLeft: 8 }}>{task.operation}</span>
                </div>
              ))}
            </section>

            {/* TRACE */}
            <section style={{ marginBottom: 30 }}>
              <h2 style={{ margin: "0 0 12px", fontSize: 16, color: "#e5e7eb" }}>Execution Trace</h2>
              {visibleSteps.length < data.result.trace.length && (
                <div style={{ color: "#94a3b8", fontSize: 13, marginBottom: 10 }}>Executing…</div>
              )}
              {visibleSteps.map((step) => (
                <div
                  key={step.task_id}
                  onClick={() => setSelectedStep(step)}
                  style={{
                    background: selectedStep?.task_id === step.task_id ? "#0f2744" : "#020617",
                    border: "1px solid",
                    borderColor: selectedStep?.task_id === step.task_id
                      ? "#6366f1"
                      : step.status === "success" ? "#16a34a" : "#dc2626",
                    borderRadius: 6,
                    padding: 10,
                    marginBottom: 10,
                    fontSize: 14,
                    opacity: 1,
                    animation: "fadeIn 0.3s ease",
                    cursor: "pointer",
                  }}
                >
                  <div>
                    <strong style={{ color: "#e5e7eb" }}>{step.task_id}</strong>
                    <span style={{ color: "#94a3b8", marginLeft: 8 }}>{step.status}</span>
                  </div>

                  {step.error && (
                    <div style={{ color: "#f87171", marginTop: 5 }}>
                      {step.error}
                    </div>
                  )}

                  <details style={{ marginTop: 8 }}>
                    <summary style={{ cursor: "pointer", color: "#94a3b8", fontSize: 13 }}>
                      Details
                    </summary>
                    <pre style={{ marginTop: 8, color: "#e5e7eb", fontSize: 12, overflowX: "auto" }}>
                      {JSON.stringify(step, null, 2)}
                    </pre>
                  </details>
                </div>
              ))}
            </section>

            {/* STEP INSPECTOR */}
            {selectedStep && (
              <section style={{ marginBottom: 30 }}>
                <h2 style={{ margin: "0 0 12px", fontSize: 16, color: "#e5e7eb" }}>Step Inspector</h2>
                <div
                  style={{
                    background: "#020617",
                    border: "1px solid #334155",
                    borderRadius: 6,
                    padding: 16,
                    fontSize: 13,
                  }}
                >
                  <div style={{ marginBottom: 10 }}>
                    <span style={{ color: "#94a3b8" }}>task_id</span>
                    <span style={{ color: "#e5e7eb", marginLeft: 12 }}>
                      <strong>{selectedStep.task_id}</strong>
                    </span>
                  </div>
                  <div style={{ marginBottom: 16 }}>
                    <span style={{ color: "#94a3b8" }}>status</span>
                    <span style={{ marginLeft: 12, color: selectedStep.status === "success" ? "#4ade80" : "#f87171" }}>
                      {selectedStep.status}
                    </span>
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <div style={{ color: "#94a3b8", marginBottom: 4 }}>input</div>
                    <pre style={{ margin: 0, background: "#0f172a", padding: 10, borderRadius: 4, overflowX: "auto", color: "#e5e7eb" }}>
                      {JSON.stringify(selectedStep.input, null, 2)}
                    </pre>
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <div style={{ color: "#94a3b8", marginBottom: 4 }}>output</div>
                    <pre style={{ margin: 0, background: "#0f172a", padding: 10, borderRadius: 4, overflowX: "auto", color: "#e5e7eb" }}>
                      {JSON.stringify(selectedStep.output, null, 2)}
                    </pre>
                  </div>
                  {selectedStep.error && (
                    <div>
                      <div style={{ color: "#94a3b8", marginBottom: 4 }}>error</div>
                      <div style={{ color: "#f87171" }}>{selectedStep.error}</div>
                    </div>
                  )}
                </div>
              </section>
            )}

            {/* RESULT */}
            <section style={{ marginBottom: 30 }}>
              <h2 style={{ margin: "0 0 12px", fontSize: 16, color: "#e5e7eb" }}>Final Result</h2>
              <div
                style={{
                  background: "#020617",
                  border: "1px solid #334155",
                  borderRadius: 6,
                  padding: 12,
                }}
              >
                <pre style={{ margin: 0, color: "#e5e7eb", fontSize: 13, overflowX: "auto" }}>
                  {JSON.stringify(data.result.result, null, 2)}
                </pre>
              </div>
            </section>
          </>
        )}
      </div>
    </div>
    </>
  );
}
