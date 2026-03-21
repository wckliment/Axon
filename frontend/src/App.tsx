import { useState, useEffect } from "react";
import type { ApiResponse, TraceStep } from "./types";
import InputBox from "./components/InputBox";
import TraceList from "./components/TraceList";
import StepInspector from "./components/StepInspector";

export default function App() {
  const [input, setInput] = useState("");
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [visibleSteps, setVisibleSteps] = useState<TraceStep[]>([]);
  const [selectedStep, setSelectedStep] = useState<TraceStep | null>(null);

  useEffect(() => {
    if (!data) return;
    setVisibleSteps([]);
    setSelectedStep(null);
    const trace = data.result.trace;
    trace.forEach((step, i) => {
      setTimeout(() => {
        setVisibleSteps((prev) => [...prev, step]);
      }, i * 400);
    });
    const rankingStep = trace.find((s) => s.task_id === "task_2");
    if (rankingStep) setSelectedStep(rankingStep);
  }, [data]);

  const run = async () => {
    setLoading(true);
    const res = await fetch("http://127.0.0.1:8000/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
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
            <InputBox
              value={input}
              onChange={setInput}
              onRun={run}
              loading={loading}
            />
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
              <TraceList
                steps={visibleSteps}
                total={data.result.trace.length}
                selectedId={selectedStep?.task_id ?? null}
                onSelect={setSelectedStep}
              />

              {/* STEP INSPECTOR */}
              {selectedStep && <StepInspector step={selectedStep} />}

              {/* RESULT */}
              <section style={{ marginBottom: 30 }}>
                <h2 style={{ margin: "0 0 12px", fontSize: 16, color: "#e5e7eb" }}>Final Result</h2>
                {(() => {
                  const rawSummary = (data.result.result as Record<string, unknown>)?.summary;
                  if (typeof rawSummary === "string") {
                    let cleaned = rawSummary;
                    if (cleaned.startsWith('"') && cleaned.endsWith('"')) {
                      cleaned = cleaned.slice(1, -1);
                    }
                    cleaned = cleaned.replace(/\\n/g, '\n').trim();
                    return (
                      <div style={{ maxWidth: 720, margin: "0 auto" }}>
                        <p style={{ margin: "0 0 8px", fontSize: 13, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                          Final Answer
                        </p>
                        <div
                          style={{
                            background: "#0f172a",
                            border: "1px solid #1f2937",
                            borderRadius: 8,
                            padding: "16px 18px",
                            marginTop: 12,
                            fontSize: 16,
                            lineHeight: 1.7,
                            letterSpacing: "0.2px",
                            whiteSpace: "pre-wrap",
                            color: "#e5e7eb",
                          }}
                        >
                          {cleaned}
                        </div>
                      </div>
                    );
                  }
                  return (
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
                  );
                })()}
              </section>
            </>
          )}
        </div>
      </div>
    </>
  );
}
