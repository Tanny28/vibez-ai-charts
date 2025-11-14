// src/components/FileUploader.tsx
import React, { useCallback, useState } from 'react';
import { motion } from 'framer-motion';
import { api } from '../lib/api';

interface FileUploaderProps {
  onUploadSuccess: (fileId: string, summary: any) => void;
}

export default function FileUploader({ onUploadSuccess }: FileUploaderProps) {
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<{ name: string; id: string } | null>(null);

  const handleFile = useCallback(
    async (file: File) => {
      if (!file.name.endsWith('.csv')) {
        alert('Only CSV files are allowed');
        return;
      }

      setUploading(true);
      try {
        const result = await api.upload(file);
        setUploadedFile({ name: result.filename, id: result.file_id });
        onUploadSuccess(result.file_id, result.summary);
      } catch (error) {
        console.error('Upload failed:', error);
        alert('Upload failed. Please try again.');
      } finally {
        setUploading(false);
      }
    },
    [onUploadSuccess]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);

      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFile(e.dataTransfer.files[0]);
      }
    },
    [handleFile]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      e.preventDefault();
      if (e.target.files && e.target.files[0]) {
        handleFile(e.target.files[0]);
      }
    },
    [handleFile]
  );

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const clearFile = () => {
    setUploadedFile(null);
  };

  return (
    <motion.div 
      className="bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur-xl border border-gray-800/50 rounded-lg p-6 shadow-xl shadow-blue-900/5"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h3 className="text-lg font-semibold text-gray-100 mb-4 font-mono">Data Source</h3>

      {uploadedFile ? (
        <div className="flex items-center justify-between p-4 bg-green-950/30 border border-green-800/50 rounded-lg">
          <div className="flex items-center gap-3">
            <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span className="text-sm font-medium text-green-400 font-mono">{uploadedFile.name}</span>
          </div>
          <button
            onClick={clearFile}
            className="p-1 text-green-400 hover:text-green-300 hover:bg-green-950/50 rounded transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      ) : (
        <form
          onDragEnter={handleDrag}
          onSubmit={(e) => e.preventDefault()}
        >
          <motion.div
            className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 ${
              dragActive
                ? 'border-blue-500 bg-blue-950/30 shadow-lg shadow-blue-500/50 scale-105'
                : 'border-gray-700 hover:border-blue-600 hover:shadow-lg hover:shadow-blue-900/30 bg-black/30'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            whileHover={{ scale: 1.02 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <input
              type="file"
              accept=".csv"
              onChange={handleChange}
              disabled={uploading}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            <motion.svg 
              className={`w-12 h-12 mx-auto mb-4 ${
                dragActive ? 'text-blue-400' : 'text-gray-600'
              }`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
              animate={dragActive ? { scale: [1, 1.1, 1] } : {}}
              transition={{ duration: 0.5, repeat: dragActive ? Infinity : 0 }}
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </motion.svg>
            <p className="text-sm text-gray-300 mb-1 font-mono">
              {uploading ? 'UPLOADING...' : 'DROP CSV FILE'}
            </p>
            <p className="text-xs text-gray-500 font-mono">or click to select</p>
          </motion.div>
        </form>
      )}
    </motion.div>
  );
}
