// src/components/KpiCards.tsx
import { motion } from 'framer-motion';
import { formatNumber } from '@/lib/utils';

interface KpiCardsProps {
  summary?: any;
}

export default function KpiCards({ summary }: KpiCardsProps) {
  if (!summary) return null;

  const kpis = [
    {
      label: 'ROWS',
      value: formatNumber(summary.num_rows || 0),
      color: 'text-blue-400',
      borderColor: 'border-blue-800/50',
      bgColor: 'bg-blue-950/30',
    },
    {
      label: 'NUMERIC',
      value: summary.num_numeric || 0,
      color: 'text-green-400',
      borderColor: 'border-green-800/50',
      bgColor: 'bg-green-950/30',
    },
    {
      label: 'CATEGORICAL',
      value: summary.num_categorical || 0,
      color: 'text-purple-400',
      borderColor: 'border-purple-800/50',
      bgColor: 'bg-purple-950/30',
    },
    {
      label: 'TEMPORAL',
      value: summary.has_date ? 'YES' : 'NO',
      color: 'text-orange-400',
      borderColor: 'border-orange-800/50',
      bgColor: 'bg-orange-950/30',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {kpis.map((kpi, index) => (
        <motion.div
          key={kpi.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className={`${kpi.bgColor} border ${kpi.borderColor} rounded-lg p-5`}
        >
          <div className="flex flex-col">
            <p className="text-xs text-gray-500 mb-2 font-mono tracking-wider">{kpi.label}</p>
            <p className={`text-2xl font-bold ${kpi.color} font-mono`}>{kpi.value}</p>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
