// src/components/DataQA.tsx
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { api, QAResponse } from '../lib/api';

interface DataQAProps {
  fileId: string;
}

export default function DataQA({ fileId }: DataQAProps) {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<QAResponse[]>([]);

  const handleAsk = async () => {
    if (!question.trim() || !fileId) return;

    setLoading(true);
    try {
      const result = await api.askQuestion(fileId, question);
      setResults([result, ...results]);
      setQuestion('');
    } catch (error) {
      console.error('Q&A error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  const exampleQuestions = [
    "What are the top 5 items by value?",
    "Which category has the highest total?",
    "Show me the average across all entries",
    "What's the total revenue?",
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-lg p-6"
    >
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h2 className="text-xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent font-mono">
          Ask Your Data
        </h2>
        <span className="px-2 py-1 bg-green-950/50 border border-green-800/50 rounded text-xs text-green-400 font-mono">
          AI-POWERED
        </span>
      </div>

      {/* Input */}
      <div className="mb-4">
        <div className="relative">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask anything about your data..."
            className="w-full bg-black/40 border border-gray-700 rounded-lg px-4 py-3 pr-24 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-green-600 focus:ring-1 focus:ring-green-600 font-mono text-sm"
            disabled={loading}
          />
          <button
            onClick={handleAsk}
            disabled={loading || !question.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-1.5 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 disabled:from-gray-700 disabled:to-gray-600 text-white rounded font-mono text-xs font-bold transition-all disabled:cursor-not-allowed"
          >
            {loading ? 'ASKING...' : 'ASK'}
          </button>
        </div>
      </div>

      {/* Example Questions */}
      {results.length === 0 && (
        <div className="mb-6">
          <p className="text-xs text-gray-500 font-mono mb-2">TRY ASKING:</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {exampleQuestions.map((q, index) => (
              <button
                key={index}
                onClick={() => setQuestion(q)}
                className="text-left bg-black/30 border border-gray-800 hover:border-green-700 hover:bg-green-950/20 rounded px-3 py-2 text-xs text-gray-400 hover:text-green-300 transition-all group"
              >
                <span className="text-green-500 mr-2 group-hover:text-green-400">→</span>
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Results */}
      <AnimatePresence>
        {results.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs text-gray-500 font-mono">Q&A HISTORY</p>
              <button
                onClick={() => setResults([])}
                className="text-xs text-gray-500 hover:text-gray-300 font-mono"
              >
                CLEAR
              </button>
            </div>

            {results.map((result, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="bg-black/40 border border-gray-800 rounded-lg p-4 space-y-3"
              >
                {/* Question */}
                <div className="flex items-start gap-2">
                  <svg className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-sm text-blue-300 font-medium">{result.question}</p>
                </div>

                {/* Answer */}
                <div className="flex items-start gap-2 pl-6">
                  <svg className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div className="flex-1">
                    <p className="text-sm text-gray-200 leading-relaxed whitespace-pre-wrap">{result.answer}</p>

                    {/* Success Indicator */}
                    {result.success && (
                      <div className="mt-2">
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-mono bg-green-950/30 border border-green-800/50 text-green-400">
                          <span className="w-1.5 h-1.5 rounded-full bg-current"></span>
                          AI RESPONSE
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
