// src/components/InsightsPanel.tsx
import { motion } from 'framer-motion';

interface Insight {
  category: string;
  icon: string;
  title: string;
  metrics: Record<string, any>;
  summary: string;
  recommendation: string;
}

interface InsightsPanelProps {
  insights: Insight[];
  autoCharts: Array<{
    title: string;
    type: string;
    prompt: string;
  }>;
  onSelectChart: (prompt: string) => void;
  aiStory?: string;  // NEW: AI-generated narrative
  aiSuggestions?: string[];  // NEW: AI follow-up questions
}

export default function InsightsPanel({ insights, autoCharts, onSelectChart, aiStory, aiSuggestions }: InsightsPanelProps) {
  if (!insights || insights.length === 0) return null;

  return (
    <div className="space-y-6">
      {/* AI Story Section - NEW! */}
      {aiStory && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-blue-950/30 to-purple-950/30 border border-blue-800/50 rounded-lg p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <h2 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent font-mono">
              AI Data Story
            </h2>
            <span className="px-2 py-1 bg-blue-950/50 border border-blue-800/50 rounded text-xs text-blue-400 font-mono">
              POWERED BY GPT-4
            </span>
          </div>
          
          <div className="bg-black/40 border border-blue-900/30 rounded-lg p-5">
            <p className="text-gray-200 leading-relaxed whitespace-pre-line">{aiStory}</p>
          </div>

          {/* AI Suggestions */}
          {aiSuggestions && aiSuggestions.length > 0 && (
            <div className="mt-4">
              <p className="text-xs text-blue-400 font-mono mb-2">💡 AI-SUGGESTED FOLLOW-UP QUESTIONS</p>
              <div className="space-y-2">
                {aiSuggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => onSelectChart(suggestion)}
                    className="w-full text-left bg-blue-950/20 hover:bg-blue-950/40 border border-blue-800/30 hover:border-blue-600/50 rounded px-4 py-2 text-sm text-gray-300 hover:text-blue-300 transition-all group"
                  >
                    <span className="text-blue-500 mr-2 group-hover:text-blue-400">→</span>
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* Insights Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-lg p-6"
      >
        <div className="flex items-center gap-2 mb-6">
          <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          <h2 className="text-xl font-bold text-gray-100 font-mono">Business Insights</h2>
          <span className="px-2 py-1 bg-purple-950/50 border border-purple-800/50 rounded text-xs text-purple-400 font-mono">
            {insights.length} INSIGHTS
          </span>
        </div>

        <div className="space-y-4">
          {insights.map((insight, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-black/30 border border-gray-800 rounded-lg p-4 hover:border-gray-700 transition-colors"
            >
              <div className="flex items-start gap-3">
                <div className="text-2xl">{insight.icon}</div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-100 mb-2">{insight.title}</h3>
                  
                  {/* Metrics */}
                  <div className="grid grid-cols-2 gap-3 mb-3">
                    {Object.entries(insight.metrics).map(([key, value]) => (
                      <div key={key} className="bg-gray-900/50 rounded px-3 py-2">
                        <p className="text-xs text-gray-500 font-mono uppercase tracking-wider">
                          {key.replace(/_/g, ' ')}
                        </p>
                        <p className="text-sm font-bold text-blue-400 font-mono mt-1">{value}</p>
                      </div>
                    ))}
                  </div>

                  {/* Summary */}
                  <p className="text-sm text-gray-300 mb-2">{insight.summary}</p>

                  {/* Recommendation */}
                  <div className="bg-blue-950/30 border border-blue-800/50 rounded p-3">
                    <p className="text-xs text-blue-400 font-mono mb-1">RECOMMENDATION</p>
                    <p className="text-sm text-gray-200">{insight.recommendation}</p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Auto-Chart Suggestions */}
      {autoCharts && autoCharts.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-lg p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
            <h2 className="text-xl font-bold text-gray-100 font-mono">Suggested Visualizations</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {autoCharts.map((chart, index) => (
              <button
                key={index}
                onClick={() => onSelectChart(chart.prompt)}
                className="bg-black/30 border border-gray-800 rounded-lg p-4 text-left hover:border-green-600 hover:bg-green-950/20 transition-all group"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-semibold text-gray-100">{chart.title}</h3>
                  <span className="px-2 py-1 bg-gray-800 group-hover:bg-green-950/50 border border-gray-700 group-hover:border-green-800/50 rounded text-xs text-gray-400 group-hover:text-green-400 font-mono transition-colors">
                    {chart.type.replace('_', ' ').toUpperCase()}
                  </span>
                </div>
                <p className="text-xs text-gray-500 font-mono">{chart.prompt}</p>
              </button>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
