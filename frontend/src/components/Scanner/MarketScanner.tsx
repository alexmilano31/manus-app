import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';

interface Opportunity {
  symbol: string;
  name: string;
  current_price: number;
  condition: string;
  platform: string;
  rsi_1h?: number;
  rsi_4h?: number;
  rsi_1d?: number;
  funding_rate?: number;
  next_funding_time?: string;
  volume_24h?: number;
  volume_change?: number;
  timeframe?: string;
}

const MarketScanner: React.FC = () => {
  const [scannerType, setScannerType] = React.useState<string>('all');
  
  const { data, isLoading, error } = useQuery(
    ['opportunities', scannerType],
    async () => {
      const response = await axios.get(`/api/market/opportunities?type=${scannerType}`);
      return response.data;
    },
    {
      refetchInterval: 60000, // Rafraîchir toutes les minutes
    }
  );

  const handleScannerTypeChange = (type: string) => {
    setScannerType(type);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-white">Recherche d'opportunités...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-500">Erreur lors de la recherche d'opportunités</div>
      </div>
    );
  }

  const opportunities: Opportunity[] = data?.opportunities || [];

  return (
    <div className="bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-white">Scanner de Marché</h2>
        <div className="flex space-x-2">
          <button 
            className={`px-3 py-1 rounded-md text-sm ${scannerType === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
            onClick={() => handleScannerTypeChange('all')}
          >
            Tous
          </button>
          <button 
            className={`px-3 py-1 rounded-md text-sm ${scannerType === 'rsi' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
            onClick={() => handleScannerTypeChange('rsi')}
          >
            RSI
          </button>
          <button 
            className={`px-3 py-1 rounded-md text-sm ${scannerType === 'funding' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
            onClick={() => handleScannerTypeChange('funding')}
          >
            Funding
          </button>
          <button 
            className={`px-3 py-1 rounded-md text-sm ${scannerType === 'volume' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
            onClick={() => handleScannerTypeChange('volume')}
          >
            Volume
          </button>
        </div>
      </div>
      
      {opportunities.length === 0 ? (
        <div className="text-center py-8 text-gray-400">
          Aucune opportunité détectée pour le moment
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-700">
            <thead>
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Actif</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Prix</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Condition</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Détails</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Plateforme</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {opportunities.map((opportunity, index) => (
                <tr key={index} className="hover:bg-gray-700">
                  <td className="px-4 py-3 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="ml-2">
                        <div className="text-sm font-medium text-white">{opportunity.symbol}</div>
                        <div className="text-xs text-gray-400">{opportunity.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-300">
                    {opportunity.current_price.toLocaleString('fr-FR', { style: 'currency', currency: 'USD' })}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-left">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      opportunity.condition.includes('survendu') || opportunity.condition.includes('négatif') ? 
                      'bg-green-900 text-green-300' : 
                      opportunity.condition.includes('suracheté') || opportunity.condition.includes('positif') ? 
                      'bg-red-900 text-red-300' : 
                      'bg-blue-900 text-blue-300'
                    }`}>
                      {opportunity.condition}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right">
                    {opportunity.rsi_1h && (
                      <div className="text-gray-300">
                        RSI: {opportunity.rsi_1h} ({opportunity.timeframe})
                      </div>
                    )}
                    {opportunity.funding_rate && (
                      <div className={`${opportunity.funding_rate < 0 ? 'text-green-400' : 'text-red-400'}`}>
                        Funding: {(opportunity.funding_rate * 100).toFixed(2)}%
                      </div>
                    )}
                    {opportunity.volume_change && (
                      <div className="text-blue-400">
                        Volume: +{opportunity.volume_change}%
                      </div>
                    )}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-300">
                    {opportunity.platform}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default MarketScanner;
