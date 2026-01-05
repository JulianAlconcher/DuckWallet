import { RefreshCw } from 'lucide-react';

/**
 * Header de la aplicación.
 */
export default function Header({ date, onRefresh, isLoading, currency, onCurrencyChange }) {
  return (
    <header className="mb-8">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-4">
          {/* Logo */}
          <div className="flex items-center justify-center w-12 h-12 rounded-xl shadow-lg overflow-hidden">
            <img src="/duck.svg" alt="DuckWallet" className="w-12 h-12" />
          </div>
          
          {/* Título */}
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-white">
              DuckWallet Screener
            </h1>
            <p className="text-slate-400 text-sm">
              Top 6 con mayor fortaleza técnica
            </p>
          </div>
        </div>

        {/* Acciones */}
        <div className="flex items-center gap-4">
          {/* Toggle USD/ARS */}
          <div className="flex items-center bg-slate-700 rounded-lg p-1">
            <button
              onClick={() => onCurrencyChange('ARS')}
              className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                currency === 'ARS'
                  ? 'bg-primary-500 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              ARS
            </button>
            <button
              onClick={() => onCurrencyChange('USD')}
              className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                currency === 'USD'
                  ? 'bg-primary-500 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              USD
            </button>
          </div>

          {date && (
            <span className="text-sm text-slate-400 hidden md:block">
              Actualizado: {(() => {
                // Parsear la fecha correctamente para evitar problemas de zona horaria
                const [year, month, day] = date.split('-').map(Number);
                const dateObj = new Date(year, month - 1, day);
                return dateObj.toLocaleDateString('es-AR', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                });
              })()}
            </span>
          )}
          
          <button
            onClick={onRefresh}
            disabled={isLoading}
            className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            Actualizar
          </button>
        </div>
      </div>
    </header>
  );
}
