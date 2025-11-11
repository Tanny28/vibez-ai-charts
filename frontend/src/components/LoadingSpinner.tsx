// src/components/LoadingSpinner.tsx
import { motion } from 'framer-motion';

export default function LoadingSpinner() {
  return (
    <div className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-lg p-12">
      <div className="flex flex-col items-center justify-center">
        <motion.div
          className="relative w-16 h-16 mb-4"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        >
          <div className="absolute inset-0 border-4 border-gray-800 rounded-full" />
          <div className="absolute inset-0 border-4 border-transparent border-t-blue-500 rounded-full" />
        </motion.div>
        <p className="text-gray-400 font-mono text-sm">PROCESSING QUERY...</p>
        <div className="flex gap-1 mt-3">
          <motion.div 
            className="w-2 h-2 bg-blue-500 rounded-full"
            animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 1.5, repeat: Infinity, delay: 0 }}
          />
          <motion.div 
            className="w-2 h-2 bg-blue-500 rounded-full"
            animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 1.5, repeat: Infinity, delay: 0.3 }}
          />
          <motion.div 
            className="w-2 h-2 bg-blue-500 rounded-full"
            animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 1.5, repeat: Infinity, delay: 0.6 }}
          />
        </div>
      </div>
    </div>
  );
}
