import React, { useState, useEffect } from 'react';
import { portfolioService } from '../services/api';

interface Balance {
  total: number;
  variation: number;
  currency: string;
}

interface Transaction {
  id: number;
  date: string;
  type: string;
  amount: number;
  status: string;
}

const Dashboard: React.FC = () => {
  const [balance, setBalance] = useState<Balance | null>(null);
  const [history, setHistory] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Récupérer le solde du portfolio
      const balanceData = await portfolioService.getBalance();
      setBalance(balanceData);
      
      // Récupérer l'historique
      const historyData = await portfolioService.getHistory();
      setHistory(historyData);
      
    } catch (err: any) {
      console.error('Error fetching portfolio data:', err);
      setError(err.message || 'Une erreur est survenue');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p className="font-bold">Erreur</p>
          <p>{error}</p>
          <button 
            onClick={fetchPortfolioData}
            className="mt-2 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      
      {/* Section Balance */}
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Solde du Portfolio</h2>
        {balance && (
          <div>
            <p className="text-3xl font-bold text-green-600">
              ${balance.total?.toFixed(2) || '0.00'}
            </p>
            <p className="text-gray-600">
              Variation: {balance.variation?.toFixed(2) || '0.00'}%
            </p>
          </div>
        )}
      </div>
      
      {/* Section Historique */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Historique des transactions</h2>
        {history.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full table-auto">
              <thead>
                <tr className="bg-gray-100">
                  <th className="px-4 py-2 text-left">Date</th>
                  <th className="px-4 py-2 text-left">Type</th>
                  <th className="px-4 py-2 text-left">Montant</th>
                  <th className="px-4 py-2 text-left">Statut</th>
                </tr>
              </thead>
              <tbody>
                {history.map((transaction) => (
                  <tr key={transaction.id} className="border-b">
                    <td className="px-4 py-2">
                      {new Date(transaction.date).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-2">{transaction.type}</td>
                    <td className="px-4 py-2">${transaction.amount.toFixed(2)}</td>
                    <td className="px-4 py-2">
                      <span className={`px-2 py-1 rounded text-xs ${
                        transaction.status === 'completed' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {transaction.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500">Aucune transaction trouvée</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;