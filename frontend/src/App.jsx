import { useState, useEffect, useCallback } from 'react';
import { getTop5Cedears } from './services/api';
import CedearCard from './components/CedearCard';
import Header from './components/Header';
import Disclaimer from './components/Disclaimer';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';

function App() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currency, setCurrency] = useState('ARS'); // Por defecto ARS

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await getTop5Cedears(true);
      setData(result);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError(
        err.response?.data?.detail || 
        'No se pudo conectar con el servidor. Verifique que el backend esté corriendo.'
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800">
      {/* Background decorativo */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-500/10 rounded-full blur-3xl" />
        <div className="absolute top-1/2 -left-40 w-80 h-80 bg-primary-600/10 rounded-full blur-3xl" />
      </div>

      {/* Contenido principal */}
      <div className="relative z-10 container mx-auto px-4 py-8 max-w-6xl">
        <Header 
          date={data?.date} 
          onRefresh={fetchData} 
          isLoading={isLoading}
          currency={currency}
          onCurrencyChange={setCurrency}
        />

        {/* Estado de carga */}
        {isLoading && (
          <LoadingSpinner message="Analizando indicadores técnicos..." />
        )}

        {/* Error */}
        {error && !isLoading && (
          <ErrorMessage message={error} onRetry={fetchData} />
        )}

        {/* Lista de CEDEARs */}
        {!isLoading && !error && data?.top5 && (
          <>
            {/* Indicador de score */}
            <div className="flex items-center justify-center gap-6 mb-6 text-xs text-slate-400">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-success-500" />
                <span>Score 8-10</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-primary-500" />
                <span>Score 5-7</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                <span>Score 3-4</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-slate-600" />
                <span>Score 0-2</span>
              </div>
            </div>

            {/* Grid de tarjetas */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data.top5.map((cedear, index) => (
                <CedearCard 
                  key={cedear.cedear} 
                  cedear={cedear} 
                  rank={index + 1}
                  currency={currency}
                />
              ))}
            </div>

            {/* Metodología */}
           
          </>
        )}

        {/* Footer */}
        <footer className="mt-12 text-center text-slate-500 text-sm">
          <p>
            DuckWallet Screener v1.0 • Datos de mercado via yfinance
          </p>
          <p className="mt-1">
            Análisis basado en acciones subyacentes (NASDAQ/NYSE) en USD
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
