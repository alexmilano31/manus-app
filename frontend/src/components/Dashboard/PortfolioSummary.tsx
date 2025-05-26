import React from 'react';

interface PortfolioSummaryProps {
  totalBalance: number;
  dailyChange: number;
  dailyChangePercent: number;
  weeklyChange: number;
  weeklyChangePercent: number;
  monthlyChange: number;
  monthlyChangePercent: number;
}

const PortfolioSummary: React.FC<PortfolioSummaryProps> = ({
  totalBalance,
  dailyChange,
  dailyChangePercent,
  weeklyChange,
  weeklyChangePercent,
  monthlyChange,
  monthlyChangePercent
}) => {
  return (
    <div className="bg-gray-800 rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-white mb-4">Résumé du Portefeuille</h2>
      
      <div className="mb-6">
        <p className="text-gray-400 text-sm">Valeur Totale</p>
        <p className="text-3xl font-bold text-white">{totalBalance.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}</p>
      </div>
      
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-gray-700 rounded-lg p-3">
          <p className="text-gray-400 text-xs">24h</p>
          <p className={`text-lg font-semibold ${dailyChange >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {dailyChange.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}
          </p>
          <p className={`text-sm ${dailyChangePercent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {dailyChangePercent >= 0 ? '+' : ''}{dailyChangePercent.toFixed(2)}%
          </p>
        </div>
        
        <div className="bg-gray-700 rounded-lg p-3">
          <p className="text-gray-400 text-xs">7j</p>
          <p className={`text-lg font-semibold ${weeklyChange >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {weeklyChange.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}
          </p>
          <p className={`text-sm ${weeklyChangePercent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {weeklyChangePercent >= 0 ? '+' : ''}{weeklyChangePercent.toFixed(2)}%
          </p>
        </div>
        
        <div className="bg-gray-700 rounded-lg p-3">
          <p className="text-gray-400 text-xs">30j</p>
          <p className={`text-lg font-semibold ${monthlyChange >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {monthlyChange.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}
          </p>
          <p className={`text-sm ${monthlyChangePercent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {monthlyChangePercent >= 0 ? '+' : ''}{monthlyChangePercent.toFixed(2)}%
          </p>
        </div>
      </div>
    </div>
  );
};

export default PortfolioSummary;
