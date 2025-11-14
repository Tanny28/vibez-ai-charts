// src/components/PromptBox.tsx
import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface PromptBoxProps {
  onSubmit: (goal: string, insight: string) => void;
  loading?: boolean;
}

const INSIGHTS = ['Auto', 'Trend', 'Comparison', 'Distribution', 'Correlation', 'Composition', 'Ranking', 'Geospatial'];

export default function PromptBox({ onSubmit, loading }: PromptBoxProps) {
  const [goal, setGoal] = useState('');
  const [insight, setInsight] = useState('Auto');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (goal.trim()) {
      onSubmit(goal, insight);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur-xl border border-gray-800/50 rounded-lg p-6 shadow-xl shadow-black/20"
    >
      <div className="flex items-center gap-2 mb-4">
        <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <h2 className="text-lg font-semibold text-gray-100 font-mono">Query Interface</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="goal" className="block text-xs font-medium text-gray-400 mb-2 font-mono uppercase tracking-wider">
            Natural Language Query
          </label>
          <textarea
            id="goal"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="describe your visualization intent..."
            className="w-full px-4 py-3 bg-black/50 backdrop-blur-sm border border-gray-700 rounded-md focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 focus:shadow-lg focus:shadow-blue-500/20 resize-none text-gray-100 placeholder-gray-600 font-mono text-sm transition-all"
            rows={3}
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="insight" className="block text-xs font-medium text-gray-400 mb-2 font-mono uppercase tracking-wider">
            Chart Type Override
          </label>
          <select
            id="insight"
            value={insight}
            onChange={(e) => setInsight(e.target.value)}
            className="w-full px-4 py-2 bg-black/50 backdrop-blur-sm border border-gray-700 rounded-md focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 focus:shadow-lg focus:shadow-blue-500/20 text-gray-100 font-mono text-sm transition-all"
            disabled={loading}
          >
            {INSIGHTS.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        <motion.button
          type="submit"
          disabled={loading || !goal.trim()}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-md font-medium hover:from-blue-500 hover:to-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all font-mono text-sm tracking-wider shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:shadow-xl"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              PROCESSING...
            </span>
          ) : (
            'EXECUTE QUERY'
          )}
        </motion.button>
      </form>
    </motion.div>
  );
}
