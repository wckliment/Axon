import type { TraceStep } from "../types";
import { getLabel } from "../taskLabels";

type Props = {
  step: TraceStep;
};

type Scoring = {
  score: number;
  scoring: {
    keyword: number;
    query: number;
    quality: number;
    fragment_penalty: number;
  };
};

type FilterDocumentsOutput = {
  documents: string[];
  scoring: Scoring[];
};

function ScoreBar({ value, max = 1 }: { value: number; max?: number }) {
  const pct = Math.min((value / max) * 100, 100);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <div
        style={{
          flex: 1,
          height: 4,
          background: "#1e293b",
          borderRadius: 2,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${pct}%`,
            height: "100%",
            background: "#6366f1",
            borderRadius: 2,
          }}
        />
      </div>
      <span style={{ color: "#e5e7eb", fontSize: 12, minWidth: 36, textAlign: "right" }}>
        {value.toFixed(3)}
      </span>
    </div>
  );
}

function SynthesisView({ output }: { output: unknown }) {
  const summary =
    output != null &&
    typeof output === "object" &&
    "summary" in output &&
    typeof (output as Record<string, unknown>).summary === "string"
      ? (output as Record<string, string>).summary
      : null;

  if (!summary) {
    return (
      <pre style={{ margin: 0, background: "#0f172a", padding: 10, borderRadius: 4, overflowX: "auto", color: "#e5e7eb", fontSize: 12 }}>
        {JSON.stringify(output, null, 2)}
      </pre>
    );
  }

  return (
    <div>
      <div style={{ color: "#64748b", fontSize: 11, marginBottom: 8 }}>Final Answer</div>
      <div
        style={{
          color: "#e5e7eb",
          fontSize: 17,
          lineHeight: 1.6,
          maxWidth: 760,
          whiteSpace: "pre-wrap",
          marginTop: 8,
        }}
      >
        {summary}
      </div>
    </div>
  );
}

function FilterDocumentsView({ output }: { output: FilterDocumentsOutput }) {
  const { documents, scoring } = output;
  const hasScoring =
    Array.isArray(scoring) && scoring.length === documents.length;

  return (
    <div>
      {documents.map((doc, i) => {
        const s = hasScoring ? scoring[i] : null;
        const isTop = i === 0;
        return (
          <div
            key={i}
            style={{
              background: isTop ? "#0f2744" : "#020617",
              border: `1px solid ${isTop ? "#6366f1" : "#1e293b"}`,
              borderRadius: 6,
              padding: 14,
              marginBottom: 10,
            }}
          >
            {/* Header row */}
            <div
              style={{
                display: "flex",
                alignItems: "baseline",
                gap: 12,
                marginBottom: 10,
              }}
            >
              <span
                style={{
                  fontSize: 11,
                  fontWeight: "bold",
                  color: isTop ? "#818cf8" : "#475569",
                  textTransform: "uppercase",
                  letterSpacing: 1,
                }}
              >
                Rank {i + 1}
              </span>
              {s && (
                <span style={{ color: "#94a3b8", fontSize: 12 }}>
                  Score:{" "}
                  <strong style={{ color: isTop ? "#a5b4fc" : "#e5e7eb" }}>
                    {s.score.toFixed(2)}
                  </strong>
                </span>
              )}
            </div>

            {/* Breakdown */}
            {s && (
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "110px 1fr",
                rowGap: 5,
                columnGap: 8,
                marginBottom: 12,
                fontSize: 12,
              }}
            >
              {(
                [
                  ["keyword", s.scoring.keyword],
                  ["query", s.scoring.query],
                  ["quality", s.scoring.quality],
                  ["fragment_penalty", s.scoring.fragment_penalty],
                ] as [string, number][]
              ).map(([label, val]) => (
                <>
                  <span key={label + "_label"} style={{ color: "#64748b", alignSelf: "center" }}>
                    {label}
                  </span>
                  <ScoreBar key={label + "_bar"} value={val} />
                </>
              ))}
            </div>
            )}

            {/* Preview */}
            <div style={{ color: "#64748b", fontSize: 11, marginBottom: 4 }}>preview</div>
            <pre
              style={{
                margin: 0,
                fontFamily: "monospace",
                fontSize: 12,
                color: "#94a3b8",
                background: "#0a0f1e",
                padding: "8px 10px",
                borderRadius: 4,
                overflowX: "auto",
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
              }}
            >
              {doc.slice(0, 200)}
              {doc.length > 200 && (
                <span style={{ color: "#475569" }}>…</span>
              )}
            </pre>
          </div>
        );
      })}
    </div>
  );
}

function JsonView({ label, value }: { label: string; value: unknown }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ color: "#64748b", fontSize: 11, marginBottom: 4 }}>{label}</div>
      <pre
        style={{
          margin: 0,
          background: "#0f172a",
          padding: 10,
          borderRadius: 4,
          overflowX: "auto",
          color: "#e5e7eb",
          fontSize: 12,
        }}
      >
        {JSON.stringify(value, null, 2)}
      </pre>
    </div>
  );
}

export default function StepInspector({ step }: Props) {
  const isFilterDocs = step.task_id === "task_2";

  return (
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
        {/* Meta */}
        <div style={{ display: "flex", gap: 20, marginBottom: 16 }}>
          <div>
            <span style={{ color: "#64748b", fontSize: 11 }}>step</span>
            <div style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
              <span style={{ color: "#e5e7eb", fontWeight: "bold" }}>{getLabel(step.task_id)}</span>
              <span style={{ color: "#475569", fontSize: 11 }}>{step.task_id}</span>
            </div>
          </div>
          <div>
            <span style={{ color: "#64748b", fontSize: 11 }}>status</span>
            <div style={{ color: step.status === "success" ? "#4ade80" : "#f87171" }}>
              {step.status}
            </div>
          </div>
        </div>

        {/* Input always as JSON */}
        <JsonView label="input" value={step.input} />

        {/* Output: structured per step, JSON fallback */}
        <div style={{ marginBottom: 12 }}>
          <div style={{ color: "#64748b", fontSize: 11, marginBottom: 8 }}>output</div>
          {(() => {
            if (isFilterDocs) {
              return (
                <>
                  <p style={{ margin: "0 0 10px", color: "#64748b", fontSize: 12 }}>
                    Top documents ranked by query relevance, content quality, and completeness
                  </p>
                  <FilterDocumentsView output={step.output as FilterDocumentsOutput} />
                </>
              );
            }

            if (step.task_id === "task_3") {
              const rawSummary = (step.output as Record<string, unknown>)?.summary;
              if (typeof rawSummary === "string") {
                let summary = rawSummary;
                if (summary.startsWith('"') && summary.endsWith('"')) {
                  summary = summary.slice(1, -1);
                }
                summary = summary.replace(/\\n/g, '\n').trim();
                return (
                  <div style={{ marginTop: 20, maxWidth: 720, margin: "20px auto 0" }}>
                    <h3 style={{ margin: "0 0 8px", fontSize: 13, color: "#94a3b8", fontWeight: "normal", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                      Final Answer
                    </h3>
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
                      {summary}
                    </div>
                  </div>
                );
              }
            }

            return (
              <pre
                style={{
                  margin: 0,
                  background: "#0f172a",
                  padding: 10,
                  borderRadius: 4,
                  overflowX: "auto",
                  color: "#e5e7eb",
                  fontSize: 12,
                }}
              >
                {JSON.stringify(step.output, null, 2)}
              </pre>
            );
          })()}
        </div>

        {/* Error */}
        {step.error && (
          <div>
            <div style={{ color: "#64748b", fontSize: 11, marginBottom: 4 }}>error</div>
            <div style={{ color: "#f87171" }}>{step.error}</div>
          </div>
        )}
      </div>
    </section>
  );
}
