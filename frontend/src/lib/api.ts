// src/lib/api.ts
import axios from 'axios';

// Use environment variable in production, localhost in development
const API_BASE = import.meta.env.VITE_API_BASE_URL || 
  (import.meta.env.PROD ? '/api' : 'http://localhost:8000');

export interface RecommendRequest {
  goal: string;
  insight?: string;
  file_id?: string;
}

export interface RecommendResponse {
  vibe: string;
  constraints: {
    palette: string;
    axis: string;
    labeling: string;
    rationale: string;
  };
  rationale: string;
  chart_spec: any;
}

export interface UploadResponse {
  file_id: string;
  filename: string;
  summary: any;
}

export interface PreviewRequest {
  file_id?: string;
  vibe: string;
  x_col?: string;
  y_col?: string;
  group_col?: string;
  options?: any;
}

export interface InsightsResponse {
  file_id: string;
  insights: Array<{
    category: string;
    icon: string;
    title: string;
    metrics: Record<string, any>;
    summary: string;
    recommendation: string;
  }>;
  recommendations: string[];
  auto_charts: Array<{
    title: string;
    type: string;
    prompt: string;
  }>;
  statistics: any;
  ai_story?: string;  // NEW: AI-generated narrative
  ai_suggestions?: string[];  // NEW: AI follow-up questions
}

export interface QAResponse {
  question: string;
  answer: string;
  success: boolean;
  data_summary?: any;
}

export const api = {
  async recommend(data: RecommendRequest): Promise<RecommendResponse> {
    const response = await axios.post(`${API_BASE}/api/recommend`, data);
    return response.data;
  },

  async upload(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_BASE}/api/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async preview(data: PreviewRequest): Promise<any> {
    const response = await axios.post(`${API_BASE}/api/preview`, data);
    return response.data;
  },

  async downloadFile(fileId: string): Promise<Blob> {
    const response = await axios.get(`${API_BASE}/api/files/${fileId}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  async getInsights(fileId: string): Promise<InsightsResponse> {
    const response = await axios.get(`${API_BASE}/api/insights/${fileId}`);
    return response.data;
  },

  async askQuestion(fileId: string, question: string): Promise<QAResponse> {
    const response = await axios.post(`${API_BASE}/api/ask`, {
      file_id: fileId,
      question: question
    });
    return response.data;
  },
};
