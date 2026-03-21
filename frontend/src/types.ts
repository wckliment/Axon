export type TraceStep = {
  task_id: string;
  status: "success" | "failed";
  input: unknown;
  output: unknown | null;
  error: string | null;
};

export type Task = {
  id: string;
  operation: string;
};

export type ApiResponse = {
  plan: {
    tasks: Task[];
  };
  result: {
    result: unknown;
    trace: TraceStep[];
  };
};
