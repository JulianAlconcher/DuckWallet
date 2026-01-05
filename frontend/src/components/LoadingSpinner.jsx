/**
 * Componente de carga con animación.
 */
export default function LoadingSpinner({ message = 'Cargando...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        {/* Spinner exterior */}
        <div className="w-16 h-16 border-4 border-primary-500/30 rounded-full"></div>
        {/* Spinner animado */}
        <div className="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-primary-500 rounded-full animate-spin"></div>
      </div>
      <p className="mt-4 text-slate-400 text-sm animate-pulse">{message}</p>
    </div>
  );
}
