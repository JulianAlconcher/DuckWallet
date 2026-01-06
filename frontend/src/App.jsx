import { useState, useEffect, useCallback, useRef } from 'react';
import { getTop5Cedears } from './services/api';
import CedearCard from './components/CedearCard';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Disclaimer from './components/Disclaimer';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';

/**
 * Verifica si el mercado de EE.UU. está abierto.
 */
function isMarketOpen() {
  const now = new Date();
  const etTime = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));
  const day = etTime.getDay();
  const hours = etTime.getHours();
  const minutes = etTime.getMinutes();
  const currentMinutes = hours * 60 + minutes;
  
  const marketOpen = 9 * 60 + 30;
  const marketClose = 16 * 60;
  
  // Cerrado fines de semana o fuera de horario
  if (day === 0 || day === 6) return false;
  if (currentMinutes < marketOpen || currentMinutes >= marketClose) return false;
  
  return true;
}

function App() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currency, setCurrency] = useState('ARS'); // Por defecto ARS
  const [strategy, setStrategy] = useState('momentum'); // Estrategia seleccionada
  const [sidebarOpen, setSidebarOpen] = useState(true); // Sidebar visible
  
  // Refs para trackear datos sin causar re-renders
  const cachedDataRef = useRef({}); // { [strategy]: data }

  const fetchData = useCallback(async (force = false) => {
    const cachedData = cachedDataRef.current[strategy];
    
    // Si el mercado está cerrado y ya tenemos datos cacheados para esta estrategia, usar cache
    if (!force && !isMarketOpen() && cachedData) {
      console.log('Mercado cerrado, usando datos en cache para:', strategy);
      setData(cachedData);
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      const result = await getTop5Cedears(true, strategy);
      setData(result);
      // Guardar en cache
      cachedDataRef.current[strategy] = result;
    } catch (err) {
      console.error('Error fetching data:', err);
      setError(
        err.response?.data?.detail || 
        'No se pudo conectar con el servidor. Verifique que el backend esté corriendo.'
      );
    } finally {
      setIsLoading(false);
    }
  }, [strategy]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 flex">
      {/* Sidebar */}
      {sidebarOpen && (
        <Sidebar 
          selectedStrategy={strategy} 
          onStrategyChange={setStrategy} 
        />
      )}

      {/* Contenido principal */}
      <div className="flex-1 relative">
        {/* Background decorativo */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-500/10 rounded-full blur-3xl" />
          <div className="absolute top-1/2 -left-40 w-80 h-80 bg-primary-600/10 rounded-full blur-3xl" />
        </div>

        <div className="relative z-10 container mx-auto px-4 py-8 max-w-6xl">
          <Header 
            date={data?.date} 
            onRefresh={() => fetchData(true)} 
            isLoading={isLoading}
            currency={currency}
            onCurrencyChange={setCurrency}
            sidebarOpen={sidebarOpen}
            onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
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
            {strategy === 'global' ? (
              /* Podio Top 3 para estrategia Global */
              <div className="flex items-center justify-center gap-4 md:gap-6 min-h-[calc(100vh-300px)]">
                {/* 2do lugar - Plata */}
                {data.top5[1] && (
                  <div className="w-full md:w-80 self-center">
                    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-b from-gray-300/20 via-gray-200/10 to-gray-500/30">
                      <div className="absolute top-1 left-1/2 transform -translate-x-1/2 z-10">
                        <span className="bg-gradient-to-r from-gray-300 via-gray-100 to-gray-300 text-gray-800 text-sm font-bold px-4 py-1 rounded-full shadow-lg">
                          🥈 2do
                        </span>
                      </div>
                      <div className="p-1 pt-8">
                        <CedearCard 
                          key={data.top5[1].cedear} 
                          cedear={data.top5[1]} 
                          rank={2}
                          currency={currency}
                          strategy={strategy}
                        />
                      </div>
                      {/* Base del podio - Plata */}
                      <div className="h-12 flex items-center justify-center">
                        <span className="text-4xl font-bold text-gray-300/50">2</span>
                      </div>
                    </div>
                  </div>
                )}
                
                {/* 1er lugar - Oro */}
                {data.top5[0] && (
                  <div className="w-full md:w-80 self-center">
                    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-b from-yellow-500/25 via-yellow-400/15 to-yellow-600/40 shadow-xl shadow-yellow-500/20">
                      <div className="absolute top-1 left-1/2 transform -translate-x-1/2 z-10">
                        <span className="bg-gradient-to-r from-yellow-500 via-yellow-300 to-yellow-500 text-yellow-900 text-sm font-bold px-4 py-1 rounded-full shadow-lg animate-pulse">
                          🥇 1ro
                        </span>
                      </div>
                      <div className="p-1 pt-8">
                        <CedearCard 
                          key={data.top5[0].cedear} 
                          cedear={data.top5[0]} 
                          rank={1}
                          currency={currency}
                          strategy={strategy}
                        />
                      </div>
                      {/* Base del podio - Oro */}
                      <div className="h-20 flex items-center justify-center">
                        <span className="text-5xl font-bold text-yellow-400/50">1</span>
                      </div>
                    </div>
                  </div>
                )}
                
                {/* 3er lugar - Bronce */}
                {data.top5[2] && (
                  <div className="w-full md:w-80 self-center">
                    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-b from-amber-700/20 via-amber-600/10 to-amber-700/35">
                      <div className="absolute top-1 left-1/2 transform -translate-x-1/2 z-10">
                        <span className="bg-gradient-to-r from-amber-700 via-amber-500 to-amber-700 text-amber-100 text-sm font-bold px-4 py-1 rounded-full shadow-lg">
                          🥉 3ro
                        </span>
                      </div>
                      <div className="p-1 pt-8">
                        <CedearCard 
                          key={data.top5[2].cedear} 
                          cedear={data.top5[2]} 
                          rank={3}
                          currency={currency}
                          strategy={strategy}
                        />
                      </div>
                      {/* Base del podio - Bronce */}
                      <div className="h-6 flex items-center justify-center">
                        <span className="text-3xl font-bold text-amber-500/50">3</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              /* Grid normal para otras estrategias */
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {data.top5.map((cedear, index) => (
                  <CedearCard 
                    key={cedear.cedear} 
                    cedear={cedear} 
                    rank={index + 1}
                    currency={currency}
                    strategy={strategy}
                  />
                ))}
              </div>
            )}

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
    </div>
  );
}

export default App;
