export const TASK_LABELS: Record<string, string> = {
  task_1: "Retrieval",
  task_2: "Ranking",
  task_3: "Synthesis",
};

export function getLabel(taskId: string): string {
  return TASK_LABELS[taskId] ?? taskId;
}
