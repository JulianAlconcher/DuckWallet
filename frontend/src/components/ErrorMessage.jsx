import { AlertCircle } from 'lucide-react';

/**
 * Componente para mostrar mensajes de error.
 */
export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="card p-6 border-danger-500/50">
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0">
          <AlertCircle className="w-6 h-6 text-danger-400" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-2">
            Error al cargar datos
          </h3>
          <p className="text-slate-400 text-sm mb-4">
            {message || 'Ha ocurrido un error inesperado. Por favor, intente nuevamente.'}
          </p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium rounded-lg transition-colors"
            >
              Reintentar
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
