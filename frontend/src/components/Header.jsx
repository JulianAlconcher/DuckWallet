import { BarChart3, RefreshCw } from 'lucide-react';

/**
 * Header de la aplicación.
 */
export default function Header({ date, onRefresh, isLoading }) {
  return (
    <header className="mb-8">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-4">
          {/* Logo */}
          <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl shadow-lg">
            <BarChart3 className="w-7 h-7 text-white" />
          </div>
          
          {/* Título */}
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-white">
              DuckWallet Screener
            </h1>
            <p className="text-slate-400 text-sm">
              Top 5 con mayor fortaleza técnica
            </p>
          </div>
        </div>

        {/* Acciones */}
        <div className="flex items-center gap-4">
          {date && (
            <span className="text-sm text-slate-400">
              Actualizado: {new Date(date).toLocaleDateString('es-AR', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
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
