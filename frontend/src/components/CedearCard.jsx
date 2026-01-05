import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

/**
 * Componente para mostrar una tarjeta de CEDEAR.
 */
export default function CedearCard({ cedear, rank, currency = 'ARS' }) {
  const {
    cedear: ticker,
    company,
    score,
    daily_change_pct,
    volume_ratio,
    rsi,
    trend,
    current_price,
    price_ars,
    daily_change_pct_ars,
    price_usd,
    daily_change_pct_usd,
    score_breakdown,
  } = cedear;

  // Determinar qué precio y variación mostrar según la moneda
  const displayPrice = currency === 'ARS' 
    ? (price_ars || current_price) 
    : (price_usd || current_price);
  const displayChange = currency === 'ARS' 
    ? (daily_change_pct_ars ?? daily_change_pct) 
    : (daily_change_pct_usd ?? daily_change_pct);
  const currencySymbol = currency === 'ARS' ? '$' : 'US$';
  const priceLabel = currency === 'ARS' ? 'Precio CEDEAR (ARS)' : 'Precio CEDEAR (USD)';

  // Formatear precio según moneda
  const formatPrice = (price) => {
    if (currency === 'ARS') {
      return price.toLocaleString('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
    }
    return price.toFixed(2);
  };

  // Determinar color del score
  const getScoreColor = (score) => {
    if (score >= 8) return 'bg-success-500 text-white';
    if (score >= 5) return 'bg-primary-500 text-white';
    if (score >= 3) return 'bg-yellow-500 text-slate-900';
    return 'bg-slate-600 text-white';
  };

  // Determinar badge de tendencia
  const getTrendBadge = (trend) => {
    switch (trend) {
      case 'bullish':
        return (
          <span className="badge-success flex items-center gap-1">
            <TrendingUp size={12} />
            Alcista
          </span>
        );
      case 'bearish':
        return (
          <span className="badge-danger flex items-center gap-1">
            <TrendingDown size={12} />
            Bajista
          </span>
        );
      default:
        return (
          <span className="badge-neutral flex items-center gap-1">
            <Minus size={12} />
            Neutral
          </span>
        );
    }
  };

  // Formato para variación diaria
  const formatChange = (change) => {
    const sign = change >= 0 ? '+' : '';
    const colorClass = change >= 0 ? 'text-success-400' : 'text-danger-400';
    return <span className={colorClass}>{sign}{change.toFixed(2)}%</span>;
  };

  return (
    <div className="card-hover p-5">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {/* Ranking */}
          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-slate-700 text-slate-300 text-sm font-bold">
            #{rank}
          </div>
          
          {/* Ticker y Empresa */}
          <div>
            <h3 className="text-xl font-bold text-white">{ticker}</h3>
            <p className="text-sm text-slate-400 truncate max-w-[200px]">{company}</p>
          </div>
        </div>

        {/* Score */}
        <div className={`score-badge ${getScoreColor(score)}`}>
          {score}
        </div>
      </div>

      {/* Precio actual */}
      <div className="mb-4 pb-4 border-b border-slate-700">
        <p className="text-sm text-slate-400 mb-1">{priceLabel}</p>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-white">{currencySymbol}{formatPrice(displayPrice)}</span>
          {formatChange(displayChange)}
        </div>
        {currency === 'ARS' && !price_ars && (
          <p className="text-xs text-slate-500 mt-1">Precio ARS no disponible</p>
        )}
      </div>

      {/* Indicadores */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div>
          <p className="text-xs text-slate-400 mb-1">RSI (14)</p>
          <p className={`text-lg font-semibold ${
            rsi >= 50 && rsi <= 70 ? 'text-success-400' : 'text-slate-300'
          }`}>
            {rsi.toFixed(1)}
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-400 mb-1">Vol. Ratio</p>
          <p className={`text-lg font-semibold ${
            volume_ratio > 1 ? 'text-success-400' : 'text-slate-300'
          }`}>
            {volume_ratio.toFixed(2)}x
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-400 mb-1">Tendencia</p>
          {getTrendBadge(trend)}
        </div>
      </div>

      {/* Score Breakdown (si está disponible) */}
      {score_breakdown && (
        <details className="text-xs text-slate-400">
          <summary className="cursor-pointer hover:text-slate-300 transition-colors">
            Ver desglose del score
          </summary>
          <div className="mt-2 space-y-1 pl-2 border-l border-slate-700">
            {Object.entries(score_breakdown).map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span>{value.reason}</span>
                <span className={value.points > 0 ? 'text-success-400' : 'text-slate-500'}>
                  +{value.points}
                </span>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}
