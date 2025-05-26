import React from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  AreaChart, Area
} from 'recharts';

interface PortfolioChartProps {
  historicalData: {
    date: string;
    value: number;
    change: number;
  }[];
  timeframe: 'day' | 'week' | 'month' | 'year' | 'all';
}

const PortfolioChart: React.FC<PortfolioChartProps> = ({ historicalData, timeframe }) => {
  // Formater les données pour l'affichage
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    
    switch(timeframe) {
      case 'day':
        return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      case 'week':
        return date.toLocaleDateString('fr-FR', { weekday: 'short' });
      case 'month':
        return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
      case 'year':
        return date.toLocaleDateString('fr-FR', { month: 'short' });
      case 'all':
        return date.toLocaleDateString('fr-FR', { month: 'short', year: '2-digit' });
      default:
        return dateStr;
    }
  };

  // Calculer si la tendance est positive ou négative
  const trend = historicalData.length > 1 
    ? historicalData[historicalData.length - 1].value > historicalData[0].value 
    : true;

  return (
    <div className="bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-white">Évolution du Portefeuille</h2>
        <div className="flex space-x-2">
          <button className={`px-3 py-1 rounded-md text-sm ${timeframe === 'day' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}>24h</button>
          <button className={`px-3 py-1 rounded-md text-sm ${timeframe === 'week' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}>7j</button>
          <button className={`px-3 py-1 rounded-md text-sm ${timeframe === 'month' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}>30j</button>
          <button className={`px-3 py-1 rounded-md text-sm ${timeframe === 'year' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}>1a</button>
          <button className={`px-3 py-1 rounded-md text-sm ${timeframe === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}>Tout</button>
        </div>
      </div>
      
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={historicalData}
            margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
          >
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={trend ? "#10B981" : "#EF4444"} stopOpacity={0.8}/>
                <stop offset="95%" stopColor={trend ? "#10B981" : "#EF4444"} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="date" 
              tickFormatter={formatDate} 
              tick={{ fill: '#9CA3AF' }}
              axisLine={{ stroke: '#4B5563' }}
            />
            <YAxis 
              tick={{ fill: '#9CA3AF' }}
              axisLine={{ stroke: '#4B5563' }}
              tickFormatter={(value) => value.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', color: '#F9FAFB' }}
              formatter={(value: number) => [value.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' }), 'Valeur']}
              labelFormatter={formatDate}
            />
            <Area 
              type="monotone" 
              dataKey="value" 
              stroke={trend ? "#10B981" : "#EF4444"} 
              fillOpacity={1} 
              fill="url(#colorValue)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PortfolioChart;
