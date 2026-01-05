import { 
  Rocket, 
  Gem, 
  Shield, 
  Coins, 
  RefreshCcw,
  ChevronRight,
  Info
} from 'lucide-react';

const strategies = [
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
    available: false,
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
  return (
    <aside className="w-64 bg-slate-800/50 backdrop-blur-sm border-r border-slate-700 p-4 flex flex-col">
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
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
