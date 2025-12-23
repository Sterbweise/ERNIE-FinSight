import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface UploadResponse {
  task_id: string;
  filename: string;
  message: string;
}

export interface TaskStatus {
  task_id: string;
  status: "pending" | "processing" | "completed" | "failed";
  message?: string;
  progress?: number;
}

export interface TaskResult {
  task_id: string;
  status: "pending" | "processing" | "completed" | "failed";
  result?: any;
  error?: string;
}

export const apiService = {
  uploadWhitepaper: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post<UploadResponse>("/api/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  },

  getTaskStatus: async (taskId: string): Promise<TaskStatus> => {
    const response = await api.get<TaskStatus>(`/api/status/${taskId}`);
    return response.data;
  },

  getTaskResult: async (taskId: string): Promise<TaskResult> => {
    const response = await api.get<TaskResult>(`/api/result/${taskId}`);
    return response.data;
  },

  pollTaskStatus: async (
    taskId: string,
    onProgress?: (status: TaskStatus) => void,
    intervalMs: number = 2000
  ): Promise<TaskResult> => {
    return new Promise((resolve, reject) => {
      const poll = async () => {
        try {
          const status = await apiService.getTaskStatus(taskId);

          if (onProgress) {
            onProgress(status);
          }

          if (status.status === "completed" || status.status === "failed") {
            const result = await apiService.getTaskResult(taskId);
            resolve(result);
          } else {
            setTimeout(poll, intervalMs);
          }
        } catch (error) {
          reject(error);
        }
      };

      poll();
    });
  },

  healthCheck: async (): Promise<{
    status: string;
    ernie_configured: boolean;
  }> => {
    const response = await api.get("/api/health");
    return response.data;
  },
};

export default apiService;
