import React from 'react';

interface AssetTableProps {
  assets: {
    symbol: string;
    name: string;
    quantity: number;
    averageEntryPrice: number;
    currentPrice: number;
    totalValue: number;
    pnl: number;
    pnlPercent: number;
    change24h: number;
    platform: string;
  }[];
}

const AssetTable: React.FC<AssetTableProps> = ({ assets }) => {
  return (
    <div className="bg-gray-800 rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-bold text-white mb-4">Détail des Actifs</h2>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-700">
          <thead>
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Actif</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Quantité</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Prix Moyen</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Prix Actuel</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Valeur Totale</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">PnL</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">24h</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Plateforme</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {assets.map((asset, index) => (
              <tr key={index} className="hover:bg-gray-700">
                <td className="px-4 py-3 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="ml-2">
                      <div className="text-sm font-medium text-white">{asset.symbol}</div>
                      <div className="text-xs text-gray-400">{asset.name}</div>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-300">
                  {asset.quantity.toLocaleString('fr-FR', { maximumFractionDigits: 8 })}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-300">
                  {asset.averageEntryPrice.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-300">
                  {asset.currentPrice.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-white font-medium">
                  {asset.totalValue.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-right">
                  <div className={`text-sm font-medium ${asset.pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {asset.pnl.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}
                  </div>
                  <div className={`text-xs ${asset.pnlPercent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {asset.pnlPercent >= 0 ? '+' : ''}{asset.pnlPercent.toFixed(2)}%
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right">
                  <span className={`${asset.change24h >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {asset.change24h >= 0 ? '+' : ''}{asset.change24h.toFixed(2)}%
                  </span>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-300">
                  {asset.platform}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AssetTable;
