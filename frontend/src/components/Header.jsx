import { RefreshCw, PanelLeftClose, PanelLeft, Menu } from 'lucide-react';

/**
 * Header de la aplicación.
 */
export default function Header({ date, onRefresh, isLoading, currency, onCurrencyChange, sidebarOpen, onToggleSidebar }) {
  return (
    <header className="mb-6 md:mb-8">
      <div className="flex items-center justify-between gap-2 md:gap-4">
        <div className="flex items-center gap-2 md:gap-4">
          {/* Botón toggle sidebar */}
          <button
            onClick={onToggleSidebar}
            className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
            title={sidebarOpen ? 'Ocultar menú' : 'Mostrar menú'}
          >
            {sidebarOpen ? (
              <PanelLeftClose className="w-5 h-5 text-slate-400 hidden md:block" />
            ) : (
              <Menu className="w-5 h-5 text-slate-400" />
            )}
            {sidebarOpen && <Menu className="w-5 h-5 text-slate-400 md:hidden" />}
          </button>

          {/* Logo */}
          <div className="flex items-center justify-center w-10 h-10 md:w-12 md:h-12 rounded-xl shadow-lg overflow-hidden">
            <img src="/duck.svg" alt="DuckWallet" className="w-10 h-10 md:w-12 md:h-12" />
          </div>
          
          {/* Título */}
          <div>
            <h1 className="text-xl md:text-3xl font-bold text-white">
              DuckWallet
            </h1>
            <p className="text-slate-400 text-xs md:text-sm hidden sm:block">
              Tu radar de CEDEARs
            </p>
          </div>
        </div>

        {/* Acciones */}
        <div className="flex items-center gap-2 md:gap-4">
          {/* Toggle USD/ARS */}
          <div className="flex items-center bg-slate-700 rounded-lg p-0.5 md:p-1">
            <button
              onClick={() => onCurrencyChange('ARS')}
              className={`px-2 md:px-3 py-1 md:py-1.5 text-xs md:text-sm font-medium rounded-md transition-colors ${
                currency === 'ARS'
                  ? 'bg-primary-500 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              ARS
            </button>
            <button
              onClick={() => onCurrencyChange('USD')}
              className={`px-2 md:px-3 py-1 md:py-1.5 text-xs md:text-sm font-medium rounded-md transition-colors ${
                currency === 'USD'
                  ? 'bg-primary-500 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              USD
            </button>
          </div>

          {date && (
            <span className="text-sm text-slate-400 hidden lg:block">
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
            className="flex items-center gap-1 md:gap-2 px-2 md:px-4 py-1.5 md:py-2 bg-slate-700 hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs md:text-sm font-medium rounded-lg transition-colors"
          >
            <RefreshCw className={`w-3 h-3 md:w-4 md:h-4 ${isLoading ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">Actualizar</span>
          </button>
        </div>
      </div>
    </header>
  );
}
