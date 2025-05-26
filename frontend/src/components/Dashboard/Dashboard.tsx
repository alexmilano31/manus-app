import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';

import PortfolioSummary from '../Dashboard/PortfolioSummary';
import PortfolioChart from '../Dashboard/PortfolioChart';
import AssetTable from '../Dashboard/AssetTable';
import AssetAllocation from '../Dashboard/AssetAllocation';

// Définition des types pour résoudre les erreurs TypeScript
interface Asset {
  amount: number;
  usd_value: number;
}

interface PlatformAsset {
  entry_price?: number;
  pnl?: number;
  pnl_percent?: number;
  change_24h?: number;
}

interface Platform {
  total_usd: number;
  assets?: Record<string, PlatformAsset>;
}

interface PortfolioData {
  total_balance_usd: number;
  assets: Record<string, Asset>;
  platforms: Record<string, Platform>;
}

interface HistoricalDataPoint {
  date: string;
  value: number;
  change: number;
}

interface HistoricalData {
  data: HistoricalDataPoint[];
  daily_change?: { value: number; percent: number };
  weekly_change?: { value: number; percent: number };
  monthly_change?: { value: number; percent: number };
}

const Dashboard: React.FC = () => {
  // Récupération des données du portefeuille
  const { data: portfolioData, isLoading: portfolioLoading, error: portfolioError } = useQuery<PortfolioData>(
    'portfolioBalance',
    async () => {
      const response = await axios.get('/api/portfolio/balance');
      return response.data;
    },
    {
      refetchInterval: 60000, // Rafraîchir toutes les minutes
    }
  );

  // Récupération des données historiques
  const { data: historicalData, isLoading: historicalLoading } = useQuery<HistoricalData>(
    'portfolioHistory',
    async () => {
      const response = await axios.get('/api/portfolio/history');
      return response.data;
    }
  );

  // Données pour le graphique d'allocation
  const allocationData = React.useMemo(() => {
    if (!portfolioData?.assets) return [];
    
    // Transformer les données pour le graphique d'allocation
    return Object.entries(portfolioData.assets).map(([symbol, data], index) => ({
      name: symbol,
      value: data.usd_value,
      color: `hsl(${index * 30 % 360}, 70%, 50%)`
    }));
  }, [portfolioData]);

  // Données pour le tableau des actifs
  const assetsTableData = React.useMemo(() => {
    if (!portfolioData?.assets) return [];
    
    // Transformer les données pour le tableau des actifs
    return Object.entries(portfolioData.assets).map(([symbol, data]) => {
      // Trouver la plateforme principale pour cet actif
      let platform = '';
      let platformData: PlatformAsset | null = null;
      
      for (const [platformName, platformAssets] of Object.entries(portfolioData.platforms)) {
        if (platformAssets.assets && platformAssets.assets[symbol]) {
          platform = platformName;
          platformData = platformAssets.assets[symbol];
          break;
        }
      }
      
      return {
        symbol,
        name: symbol, // Idéalement, récupérer le nom complet depuis une API
        quantity: data.amount,
        averageEntryPrice: platformData?.entry_price || 0,
        currentPrice: data.usd_value / data.amount,
        totalValue: data.usd_value,
        pnl: platformData?.pnl || 0,
        pnlPercent: platformData?.pnl_percent || 0,
        change24h: platformData?.change_24h || 0,
        platform
      };
    });
  }, [portfolioData]);

  // Données pour le résumé du portefeuille
  const summaryData = React.useMemo(() => {
    if (!portfolioData || !historicalData) {
      return {
        totalBalance: 0,
        dailyChange: 0,
        dailyChangePercent: 0,
        weeklyChange: 0,
        weeklyChangePercent: 0,
        monthlyChange: 0,
        monthlyChangePercent: 0
      };
    }
    
    return {
      totalBalance: portfolioData.total_balance_usd,
      dailyChange: historicalData.daily_change?.value || 0,
      dailyChangePercent: historicalData.daily_change?.percent || 0,
      weeklyChange: historicalData.weekly_change?.value || 0,
      weeklyChangePercent: historicalData.weekly_change?.percent || 0,
      monthlyChange: historicalData.monthly_change?.value || 0,
      monthlyChangePercent: historicalData.monthly_change?.percent || 0
    };
  }, [portfolioData, historicalData]);

  if (portfolioLoading || historicalLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-white">Chargement des données...</div>
      </div>
    );
  }

  if (portfolioError) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-red-500">Erreur lors du chargement des données</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-white mb-6">Tableau de Bord</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-2">
          <PortfolioSummary {...summaryData} />
        </div>
        <div>
          <AssetAllocation allocation={allocationData} />
        </div>
      </div>
      
      <div className="mb-6">
        <PortfolioChart 
          historicalData={historicalData?.data || []} 
          timeframe="month" 
        />
      </div>
      
      <div>
        <AssetTable assets={assetsTableData} />
      </div>
    </div>
  );
};

export default Dashboard;
