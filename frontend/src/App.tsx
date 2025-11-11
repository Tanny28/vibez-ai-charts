// src/App.tsx
import { useState } from 'react';
import { motion } from 'framer-motion';
import PromptBox from './components/PromptBox';
import FileUploader from './components/FileUploader';
import ChartCanvas from './components/ChartCanvas';
import KpiCards from './components/KpiCards';
import ConstraintsCard from './components/ConstraintsCard';
import LoadingSpinner from './components/LoadingSpinner';
import InsightsPanel from './components/InsightsPanel';
import { useVibe } from './hooks/useVibe';
import { api } from './lib/api';

function App() {
  const [fileId, setFileId] = useState<string>('');
  const [summary, setSummary] = useState<any>(null);
  const [insights, setInsights] = useState<any>(null);
  const [loadingInsights, setLoadingInsights] = useState(false);
  const { loading, result, error, getRecommendation, reset } = useVibe();

  const handlePromptSubmit = async (goal: string, insightType: string) => {
    try {
      await getRecommendation({ 
        goal: goal,
        insight: insightType,
        file_id: fileId || undefined
      });
    } catch (err) {
      console.error('Recommendation error:', err);
    }
  };

  const handleUploadSuccess = async (uploadedFileId: string, uploadSummary: any) => {
    setFileId(uploadedFileId);
    setSummary(uploadSummary);
    
    // Automatically fetch insights when file is uploaded
    setLoadingInsights(true);
    try {
      const insightsData = await api.getInsights(uploadedFileId);
      setInsights(insightsData);
    } catch (error) {
      console.error('Failed to fetch insights:', error);
    } finally {
      setLoadingInsights(false);
    }
  };

  const handleSelectAutoChart = (prompt: string) => {
    handlePromptSubmit(prompt, 'Auto');
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-gray-100">
      {/* Header */}
      <header className="border-b border-gray-800 bg-black/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <img 
                src="/vibez-logo.png" 
                alt="Vibez AI Charts" 
                className="h-12 w-auto"
              />
              <div className="border-l border-gray-700 pl-4">
                <p className="text-xs text-gray-400 font-mono">Natural Language → Professional Visualizations</p>
              </div>
            </div>
            {result && (
              <button
                onClick={reset}
                className="px-4 py-2 text-sm font-medium text-gray-300 bg-gray-800 hover:bg-gray-700 rounded-lg transition-all border border-gray-700 hover:border-gray-600"
              >
                <span className="font-mono">New Query</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <FileUploader onUploadSuccess={handleUploadSuccess} />
            <PromptBox onSubmit={handlePromptSubmit} loading={loading} />
            {result?.constraints && (
              <ConstraintsCard constraints={result.constraints} />
            )}
          </div>

          {/* Main Canvas */}
          <div className="lg:col-span-2">
            {summary && <KpiCards summary={summary} />}
            
            {loadingInsights && (
              <div className="mb-6">
                <div className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-lg p-6 text-center">
                  <p className="text-gray-400 font-mono text-sm">ANALYZING DATA...</p>
                </div>
              </div>
            )}
            
            {insights && !loadingInsights && (
              <div className="mb-6">
                <InsightsPanel 
                  insights={insights.insights} 
                  autoCharts={insights.auto_charts}
                  onSelectChart={handleSelectAutoChart}
                />
              </div>
            )}
            
            {loading && <LoadingSpinner />}
            
            {error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="bg-red-950/50 border border-red-800 rounded-lg p-6 text-center backdrop-blur-sm"
              >
                <p className="text-red-400 font-medium font-mono">ERROR</p>
                <p className="text-red-300 text-sm mt-1 font-mono">{error}</p>
              </motion.div>
            )}
            
            {result && !loading && result.chart_spec && (
              <ChartCanvas spec={result.chart_spec} vibe={result.vibe} />
            )}

            {!loading && !result && !error && (
              <div className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-lg p-12 text-center">
                <div className="max-w-2xl mx-auto">
                  <div className="inline-block mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                  </div>
                  <h2 className="text-3xl font-bold text-gray-100 mb-3 tracking-tight">
                    Natural Language to Chart
                  </h2>
                  <p className="text-gray-400 mb-8 font-mono text-sm">
                    Upload CSV data and describe your visualization intent. 
                    ML-powered engine selects optimal chart type.
                  </p>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="bg-blue-950/30 border border-blue-800/50 p-4 rounded-lg text-left hover:bg-blue-950/50 transition-colors">
                      <p className="font-semibold text-blue-400 mb-2 font-mono text-xs">TEMPORAL</p>
                      <p className="text-gray-300 text-xs">show sales trends over time</p>
                    </div>
                    <div className="bg-green-950/30 border border-green-800/50 p-4 rounded-lg text-left hover:bg-green-950/50 transition-colors">
                      <p className="font-semibold text-green-400 mb-2 font-mono text-xs">COMPARISON</p>
                      <p className="text-gray-300 text-xs">compare revenue by region</p>
                    </div>
                    <div className="bg-purple-950/30 border border-purple-800/50 p-4 rounded-lg text-left hover:bg-purple-950/50 transition-colors">
                      <p className="font-semibold text-purple-400 mb-2 font-mono text-xs">DISTRIBUTION</p>
                      <p className="text-gray-300 text-xs">distribution of customer ages</p>
                    </div>
                    <div className="bg-orange-950/30 border border-orange-800/50 p-4 rounded-lg text-left hover:bg-orange-950/50 transition-colors">
                      <p className="font-semibold text-orange-400 mb-2 font-mono text-xs">GEOSPATIAL</p>
                      <p className="text-gray-300 text-xs">GDP by country on map</p>
                    </div>
                  </div>
                  <div className="mt-8 pt-6 border-t border-gray-800">
                    <div className="flex items-center justify-center gap-6 text-xs text-gray-500 font-mono">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                        <span>ML Active</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span>91.43% Accuracy</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span>7 Chart Types</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 pb-6 text-center text-xs text-gray-600 font-mono border-t border-gray-900 pt-6">
        <p>FastAPI • React • TensorFlow-style ML • Plotly</p>
      </footer>
    </div>
  );
}

export default App;
