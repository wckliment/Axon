type Props = {
  value: string;
  onChange: (val: string) => void;
  onRun: () => void;
  loading: boolean;
};

export default function InputBox({ value, onChange, onRun, loading }: Props) {
  return (
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
          fontFamily: "monospace",
          resize: "vertical",
        }}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Enter a task..."
      />
      <button
        onClick={onRun}
        disabled={loading}
        style={{
          background: "#6366f1",
          color: "#ffffff",
          border: "none",
          borderRadius: 6,
          padding: "10px 20px",
          fontSize: 14,
          fontFamily: "monospace",
          cursor: loading ? "not-allowed" : "pointer",
          opacity: loading ? 0.7 : 1,
          whiteSpace: "nowrap",
        }}
      >
        {loading ? "Running..." : "Run"}
      </button>
    </div>
  );
}
