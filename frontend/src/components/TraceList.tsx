import type { TraceStep } from "../types";
import { getLabel } from "../taskLabels";

type Props = {
  steps: TraceStep[];
  total: number;
  selectedId: string | null;
  onSelect: (step: TraceStep) => void;
};

export default function TraceList({ steps, total, selectedId, onSelect }: Props) {
  return (
    <section style={{ marginBottom: 30 }}>
      <h2 style={{ margin: "0 0 12px", fontSize: 16, color: "#e5e7eb" }}>Execution Trace</h2>
      {steps.length < total && (
        <div style={{ color: "#94a3b8", fontSize: 13, marginBottom: 10 }}>Executing…</div>
      )}
      {steps.map((step) => (
        <div
          key={step.task_id}
          onClick={() => onSelect(step)}
          style={{
            background: selectedId === step.task_id ? "#0f2744" : "#020617",
            border: "1px solid",
            borderColor:
              selectedId === step.task_id
                ? "#6366f1"
                : step.status === "success"
                ? "#16a34a"
                : "#dc2626",
            borderRadius: 6,
            padding: 10,
            marginBottom: 10,
            fontSize: 14,
            animation: "fadeIn 0.3s ease",
            cursor: "pointer",
          }}
        >
          <div style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
            <strong style={{ color: "#e5e7eb" }}>{getLabel(step.task_id)}</strong>
            <span style={{ color: "#475569", fontSize: 11 }}>{step.task_id}</span>
            <span style={{ color: "#94a3b8", fontSize: 12, marginLeft: "auto" }}>{step.status}</span>
          </div>
          {step.error && (
            <div style={{ color: "#f87171", marginTop: 5 }}>{step.error}</div>
          )}
        </div>
      ))}
    </section>
  );
}
