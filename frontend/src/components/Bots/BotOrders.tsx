import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';

interface BotOrder {
  id: string;
  bot_id: string;
  bot_name: string;
  exchange: string;
  symbol: string;
  type: string;
  side: string;
  price: number;
  amount: number;
  status: string;
  filled: number;
  remaining: number;
  cost: number;
  fee: number;
  created_at: string;
  updated_at: string;
  closed_at: string | null;
  pnl: number | null;
  pnl_percent: number | null;
}

interface BotOrdersProps {
  botId?: string;
}

const BotOrders: React.FC<BotOrdersProps> = ({ botId }) => {
  const [status, setStatus] = React.useState<string>('all');
  
  const { data, isLoading, error } = useQuery(
    ['botOrders', botId, status],
    async () => {
      const params: Record<string, string> = {};
      if (botId) params.bot_id = botId;
      if (status !== 'all') params.status = status;
      
      const response = await axios.get('/api/bots/orders', { params });
      return response.data;
    },
    {
      refetchInterval: 30000, // Rafraîchir toutes les 30 secondes
    }
  );

  const handleStatusChange = (newStatus: string) => {
    setStatus(newStatus);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-white">Chargement des ordres...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-500">Erreur lors du chargement des ordres</div>
      </div>
    );
  }

  const orders: BotOrder[] = data?.orders || [];

  return (
    <div className="bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-white">Ordres des Bots</h2>
        <div className="flex space-x-2">
          <button 
            className={`px-3 py-1 rounded-md text-sm ${status === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
            onClick={() => handleStatusChange('all')}
          >
            Tous
          </button>
          <button 
            className={`px-3 py-1 rounded-md text-sm ${status === 'open' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
            onClick={() => handleStatusChange('open')}
          >
            Ouverts
          </button>
          <button 
            className={`px-3 py-1 rounded-md text-sm ${status === 'closed' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
            onClick={() => handleStatusChange('closed')}
          >
            Fermés
          </button>
          <button 
            className={`px-3 py-1 rounded-md text-sm ${status === 'canceled' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
            onClick={() => handleStatusChange('canceled')}
          >
            Annulés
          </button>
        </div>
      </div>
      
      {orders.length === 0 ? (
        <div className="text-center py-8 text-gray-400">
          Aucun ordre trouvé
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-700">
            <thead>
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Bot / Actif</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Type</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Prix</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Quantité</th>
                <th className="px-4 py-3 text-center text-xs font-medium text-gray-400 uppercase tracking-wider">Statut</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">PnL</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {orders.map((order) => (
                <tr key={order.id} className="hover:bg-gray-700">
                  <td className="px-4 py-3 whitespace-nowrap">
                    <div className="flex flex-col">
                      <div className="text-sm font-medium text-white">{order.bot_name}</div>
                      <div className="text-xs text-gray-400">{order.symbol} ({order.exchange})</div>
                    </div>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      order.side === 'buy' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'
                    }`}>
                      {order.side === 'buy' ? 'Achat' : 'Vente'} {order.type}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-300">
                    {order.price.toLocaleString('fr-FR', { style: 'currency', currency: 'USD' })}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-300">
                    {order.amount.toLocaleString('fr-FR', { maximumFractionDigits: 8 })}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-center">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      order.status === 'open' ? 'bg-blue-900 text-blue-300' :
                      order.status === 'closed' ? 'bg-green-900 text-green-300' :
                      order.status === 'canceled' ? 'bg-gray-600 text-gray-300' :
                      'bg-red-900 text-red-300'
                    }`}>
                      {order.status === 'open' ? 'Ouvert' :
                       order.status === 'closed' ? 'Fermé' :
                       order.status === 'canceled' ? 'Annulé' : 'Erreur'}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right">
                    {order.pnl !== null ? (
                      <div>
                        <div className={`font-medium ${order.pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {order.pnl.toLocaleString('fr-FR', { style: 'currency', currency: 'USD' })}
                        </div>
                        <div className={`text-xs ${order.pnl_percent! >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {order.pnl_percent! >= 0 ? '+' : ''}{order.pnl_percent!.toFixed(2)}%
                        </div>
                      </div>
                    ) : (
                      <span className="text-gray-500">-</span>
                    )}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-300">
                    {new Date(order.created_at).toLocaleString('fr-FR', {
                      day: '2-digit',
                      month: '2-digit',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
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

export default BotOrders;
