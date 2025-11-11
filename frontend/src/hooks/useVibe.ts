// src/hooks/useVibe.ts
import { useState } from 'react';
import { api, RecommendRequest, RecommendResponse } from '../lib/api';

export function useVibe() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RecommendResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const getRecommendation = async (request: RecommendRequest) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.recommend(request);
      setResult(data);
      return data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to get recommendation';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
  };

  return {
    loading,
    result,
    error,
    getRecommendation,
    reset,
  };
}
