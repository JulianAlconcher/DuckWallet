import { AlertTriangle } from 'lucide-react';

/**
 * Banner de disclaimer legal.
 */
export default function Disclaimer({ text }) {
  return (
    <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mb-6">
      <div className="flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" />
        <p className="text-sm text-yellow-200/80">
          {text || 
            'Este análisis es exclusivamente informativo y educativo. No constituye asesoramiento financiero ni recomendación de inversión. Los indicadores técnicos reflejan el comportamiento pasado y no garantizan resultados futuros.'}
        </p>
      </div>
    </div>
  );
}
