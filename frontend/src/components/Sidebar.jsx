import { useState, useEffect } from 'react';
import { 
  Rocket, 
  Gem, 
  Shield, 
  Coins, 
  RefreshCcw,
  ChevronRight,
  Info,
  Clock,
  Globe
} from 'lucide-react';

/**
 * Determina si el mercado de EE.UU. está abierto.
 * NYSE/NASDAQ: 9:30 AM - 4:00 PM Eastern Time (ET)
 */
function getMarketStatus() {
  const now = new Date();
  
  // Obtener componentes de hora en Eastern Time
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    hour: 'numeric',
    minute: 'numeric',
    weekday: 'short',
    hour12: false
  });
  
  const parts = formatter.formatToParts(now);
  const hours = parseInt(parts.find(p => p.type === 'hour')?.value || '0', 10);
  const minutes = parseInt(parts.find(p => p.type === 'minute')?.value || '0', 10);
  const weekday = parts.find(p => p.type === 'weekday')?.value || '';
  
  const currentMinutes = hours * 60 + minutes;
  const isWeekend = weekday === 'Sat' || weekday === 'Sun';
  
  // Mercado abierto: Lunes a Viernes, 9:30 AM - 4:00 PM ET
  const marketOpen = 9 * 60 + 30;  // 9:30 AM = 570 minutos
  const marketClose = 16 * 60;      // 4:00 PM = 960 minutos
  
  // Fines de semana
  if (isWeekend) {
    return { isOpen: false, label: 'Mercado Cerrado', sublabel: 'Fin de semana' };
  }
  
  // Pre-market (antes de 9:30 AM ET)
  if (currentMinutes < marketOpen) {
    const remaining = marketOpen - currentMinutes;
    const hoursLeft = Math.floor(remaining / 60);
    const minsLeft = remaining % 60;
    if (hoursLeft > 0) {
      return { isOpen: false, label: 'Pre-Market', sublabel: `Abre en ${hoursLeft}h ${minsLeft}m` };
    }
    return { isOpen: false, label: 'Pre-Market', sublabel: `Abre en ${minsLeft}m` };
  }
  
  // Mercado abierto
  if (currentMinutes >= marketOpen && currentMinutes < marketClose) {
    const remaining = marketClose - currentMinutes;
    const hoursLeft = Math.floor(remaining / 60);
    const minsLeft = remaining % 60;
    return { 
      isOpen: true, 
      label: 'Mercado Abierto', 
      sublabel: `Cierra en ${hoursLeft}h ${minsLeft}m`
    };
  }
  
  // After-hours
  return { isOpen: false, label: 'Mercado Cerrado', sublabel: 'Abre mañana 9:30 ET' };
}

const strategies = [
  {
    id: 'global',
    name: 'Global',
    icon: Globe,
    description: 'CEDEARs que destacan en múltiples estrategias',
    available: true,
    color: 'text-amber-400',
    bgColor: 'bg-amber-500/20',
  },
  {
    id: 'momentum',
    name: 'Momentum',
    icon: Rocket,
    description: 'Acciones que vienen subiendo con fuerza técnica',
    available: true,
    color: 'text-primary-400',
    bgColor: 'bg-primary-500/20',
  },
  {
    id: 'value',
    name: 'Value',
    icon: Gem,
    description: 'Acciones "baratas" con buenos fundamentales',
    available: true,
    color: 'text-emerald-400',
    bgColor: 'bg-emerald-500/20',
  },
  {
    id: 'defensive',
    name: 'Defensivo',
    icon: Shield,
    description: 'Acciones estables con baja volatilidad',
    available: true,
    color: 'text-blue-400',
    bgColor: 'bg-blue-500/20',
  },
  {
    id: 'dividends',
    name: 'Dividendos',
    icon: Coins,
    description: 'Empresas que pagan buenos dividendos',
    available: false,
    color: 'text-yellow-400',
    bgColor: 'bg-yellow-500/20',
  },
  {
    id: 'contrarian',
    name: 'Contrarian',
    icon: RefreshCcw,
    description: 'Acciones sobrevendidas que pueden rebotar',
    available: false,
    color: 'text-purple-400',
    bgColor: 'bg-purple-500/20',
  },
];

export default function Sidebar({ selectedStrategy, onStrategyChange }) {
  const [marketStatus, setMarketStatus] = useState(getMarketStatus());

  // Actualizar estado del mercado cada minuto
  useEffect(() => {
    const interval = setInterval(() => {
      setMarketStatus(getMarketStatus());
    }, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <aside className="w-64 bg-slate-800 border-r border-slate-700 p-4 flex flex-col flex-shrink-0 sticky top-0 h-screen overflow-y-auto">
      {/* Indicador de mercado */}
      <div className={`mb-4 p-3 rounded-lg border ${
        marketStatus.isOpen 
          ? 'bg-success-500/10 border-success-500/30' 
          : 'bg-danger-500/10 border-danger-500/30'
      }`}>
        <div className="flex items-center gap-2">
          <div className="relative flex h-3 w-3">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
              marketStatus.isOpen ? 'bg-success-400' : 'bg-danger-400'
            }`}></span>
            <span className={`relative inline-flex rounded-full h-3 w-3 ${
              marketStatus.isOpen ? 'bg-success-500' : 'bg-danger-500'
            }`}></span>
          </div>
          <span className={`text-sm font-medium ${
            marketStatus.isOpen ? 'text-success-400' : 'text-danger-400'
          }`}>
            {marketStatus.label}
          </span>
        </div>
        <p className="text-xs text-slate-500 mt-1 ml-5">
          {marketStatus.sublabel}
        </p>
      </div>

      {/* Separador */}
      <div className="border-b border-slate-700 mb-4" />

      {/* Header del sidebar */}
      <div className="mb-6">
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-1">
          Estrategia
        </h2>
        <p className="text-xs text-slate-500">
          Elegí el tipo de análisis
        </p>
      </div>

      {/* Lista de estrategias */}
      <nav className="flex-1 space-y-2">
        {strategies.map((strategy) => {
          const Icon = strategy.icon;
          const isSelected = selectedStrategy === strategy.id;
          
          return (
            <button
              key={strategy.id}
              onClick={() => strategy.available && onStrategyChange(strategy.id)}
              disabled={!strategy.available}
              className={`
                w-full text-left p-3 rounded-lg transition-all duration-200
                ${isSelected 
                  ? `${strategy.bgColor} border border-slate-600` 
                  : 'hover:bg-slate-700/50 border border-transparent'
                }
                ${!strategy.available && 'opacity-50 cursor-not-allowed'}
              `}
            >
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${strategy.bgColor}`}>
                  <Icon className={`w-4 h-4 ${strategy.color}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`font-medium ${isSelected ? 'text-white' : 'text-slate-300'}`}>
                      {strategy.name}
                    </span>
                    {!strategy.available && (
                      <span className="text-[10px] px-1.5 py-0.5 bg-slate-600 text-slate-400 rounded">
                        Pronto
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-500 truncate mt-0.5">
                    {strategy.description}
                  </p>
                </div>
                {isSelected && (
                  <ChevronRight className="w-4 h-4 text-slate-400" />
                )}
              </div>
            </button>
          );
        })}
      </nav>

      {/* Info de la estrategia seleccionada */}
      <div className="mt-4 p-3 bg-slate-700/30 rounded-lg border border-slate-700">
        <div className="flex items-start gap-2">
          <Info className="w-4 h-4 text-primary-400 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-xs text-slate-400">
              {selectedStrategy === 'global' && (
                <>
                  <span className="text-white font-medium">Global</span> muestra CEDEARs que 
                  destacan en múltiples estrategias simultáneamente.
                </>
              )}
              {selectedStrategy === 'momentum' && (
                <>
                  <span className="text-white font-medium">Momentum</span> busca acciones con 
                  tendencia alcista, buen volumen y RSI en zona óptima.
                </>
              )}
              {selectedStrategy === 'value' && (
                <>
                  <span className="text-white font-medium">Value</span> busca acciones "baratas" 
                  con P/E bajo, buenos dividendos y ROE alto.
                </>
              )}
              {selectedStrategy === 'defensive' && (
                <>
                  <span className="text-white font-medium">Defensivo</span> busca acciones estables 
                  con beta bajo, baja volatilidad y sectores defensivos.
                </>
              )}
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
