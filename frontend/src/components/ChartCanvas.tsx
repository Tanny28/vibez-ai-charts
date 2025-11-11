// src/components/ChartCanvas.tsx
import React from 'react';
import { motion } from 'framer-motion';
import { downloadJSON } from '../lib/utils';

interface ChartCanvasProps {
  spec: any;
  vibe: string;
}

export default function ChartCanvas({ spec, vibe }: ChartCanvasProps) {
  if (!spec || !spec.data) {
    return (
      <div className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-lg p-12 flex items-center justify-center">
        <p className="text-gray-500 text-lg font-mono">NO DATA LOADED</p>
      </div>
    );
  }

  const handleDownloadSpec = () => {
    downloadJSON(spec, `chart-${vibe}-spec.json`);
  };

  // Dynamically import Plotly to avoid SSR issues
  const [Plot, setPlot] = React.useState<any>(null);

  React.useEffect(() => {
    import('react-plotly.js').then((module) => {
      setPlot(() => module.default);
    }).catch(err => {
      console.error('Failed to load Plotly:', err);
    });
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-lg p-6"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <h3 className="text-lg font-semibold text-gray-100 font-mono">Visualization Output</h3>
          <span className="px-2 py-1 bg-blue-950/50 border border-blue-800/50 rounded text-xs text-blue-400 font-mono">{vibe.toUpperCase()}</span>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleDownloadSpec}
            className="p-2 text-gray-400 hover:text-blue-400 hover:bg-gray-800 rounded transition-colors"
            title="Download Spec (JSON)"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </button>
          <button
            className="p-2 text-gray-400 hover:text-blue-400 hover:bg-gray-800 rounded transition-colors"
            title="Fullscreen"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
            </svg>
          </button>
        </div>
      </div>

      <div className="bg-black/50 border border-gray-800 rounded-lg p-4">
        {spec.library === 'plotly' && Plot ? (
          <Plot
            data={spec.data}
            layout={{
              ...spec.layout,
              autosize: true,
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0)',
              font: { color: '#e5e7eb', family: 'monospace' },
            }}
            config={{ responsive: true, displayModeBar: true }}
            style={{ width: '100%', height: '500px' }}
            useResizeHandler={true}
          />
        ) : spec.library === 'plotly' && !Plot ? (
          <div className="text-center py-12">
            <p className="text-gray-500 font-mono">LOADING CHART...</p>
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500 font-mono">
            {spec.message || 'CHART RENDERING NOT AVAILABLE'}
          </div>
        )}
      </div>
    </motion.div>
  );
}
