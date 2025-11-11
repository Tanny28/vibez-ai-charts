// src/components/ConstraintsCard.tsx
import { motion } from 'framer-motion';

interface ConstraintsCardProps {
  constraints?: any;
}

export default function ConstraintsCard({ constraints }: ConstraintsCardProps) {
  if (!constraints) return null;

  const sections = [
    {
      title: 'PALETTE',
      value: constraints.palette,
    },
    {
      title: 'AXIS',
      value: constraints.axis,
    },
    {
      title: 'LABELS',
      value: constraints.labeling,
    },
  ].filter(s => s.value);

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-lg p-6"
    >
      <h3 className="text-lg font-semibold text-gray-100 mb-4 font-mono">Design Constraints</h3>
      
      {sections.map((section) => (
        <div key={section.title} className="mb-4 last:mb-0">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-1 h-4 bg-blue-500 rounded"></div>
            <h4 className="text-xs font-medium text-gray-400 font-mono tracking-wider">{section.title}</h4>
          </div>
          <div className="pl-3">
            <p className="text-sm text-gray-300 leading-relaxed">{section.value}</p>
          </div>
        </div>
      ))}

      {constraints.rationale && (
        <div className="mt-4 pt-4 border-t border-gray-800">
          <h4 className="text-xs font-medium text-gray-400 mb-2 font-mono tracking-wider">RATIONALE</h4>
          <p className="text-sm text-gray-300 leading-relaxed">{constraints.rationale}</p>
        </div>
      )}
    </motion.div>
  );
}
