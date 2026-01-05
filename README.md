# CEDEAR Screener 🦆📊

Aplicación informativa que calcula diariamente el **Top 5 de CEDEARs con mayor fortaleza técnica**, basada en el análisis de sus acciones subyacentes en NASDAQ y NYSE.

## ⚠️ Disclaimer

> **Este sistema es exclusivamente informativo y educativo. No constituye asesoramiento financiero ni recomendación de inversión.**

## 🎯 Objetivo

Analizar indicadores técnicos de acciones subyacentes de CEDEARs para identificar aquellas que presentan mayor fortaleza técnica según criterios objetivos y transparentes.

## 📊 Metodología de Scoring

Cada CEDEAR recibe un puntaje técnico (máximo 10 puntos) basado en:

| Criterio | Puntos | Condición |
|----------|--------|-----------|
| Variación diaria | +3 | > 2% |
| Volumen | +2 | > promedio 30 días |
| RSI (14) | +2 | Entre 50 y 70 |
| Precio vs SMA | +2 | Precio > SMA 20 |
| Tendencia | +1 | Alcista (últimos 5 días) |

## 🏗️ Arquitectura

### Backend (Python + FastAPI)
- **Datos de mercado**: yfinance
- **Análisis técnico**: ta-lib, pandas
- **API REST**: FastAPI con documentación automática

### Frontend (React + Vite)
- **Estilos**: TailwindCSS
- **HTTP Client**: Axios
- **Íconos**: Lucide React

## 🚀 Instalación y Ejecución

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```

## 📡 API Endpoints

| Endpoint | Descripción |
|----------|-------------|
| `GET /api/v1/top5-cedears` | Top 5 CEDEARs con mayor score |
| `GET /api/v1/cedears` | Todos los CEDEARs analizados |
| `GET /api/v1/cedears/{ticker}` | Detalle de un CEDEAR |
| `GET /api/v1/universe` | Lista de CEDEARs disponibles |
| `GET /api/v1/health` | Estado del servicio |

## 📦 Ejemplo de Respuesta

```json
{
  "date": "2024-01-15",
  "disclaimer": "Este análisis es informativo y educativo...",
  "top5": [
    {
      "cedear": "NVDA",
      "company": "NVIDIA Corporation",
      "score": 9,
      "daily_change_pct": 3.45,
      "volume_ratio": 1.82,
      "rsi": 62.5,
      "trend": "bullish",
      "current_price": 547.20
    }
  ]
}
```

## 🔧 Configuración

### Variables de Entorno (Backend)

Copiar `.env.example` a `.env`:

```env
ALPHA_VANTAGE_API_KEY=your_key_here  # Opcional
DEBUG=true
```

### Universo de CEDEARs

El universo de activos se configura en `backend/app/config.py`:

```python
CEDEAR_UNIVERSE = {
    "AAPL": {"company": "Apple Inc.", "ratio": 10},
    "MSFT": {"company": "Microsoft Corporation", "ratio": 5},
    # ...
}
```

## 📈 Indicadores Técnicos

- **RSI (14)**: Índice de Fuerza Relativa
- **SMA 20**: Media Móvil Simple de 20 períodos
- **Volumen Ratio**: Volumen actual / Promedio 30 días
- **Tendencia**: Basada en variación de últimos 5 días

## 🚧 Roadmap

- [ ] Integrar precio local del CEDEAR
- [ ] Ajuste por ratio de conversión
- [ ] Análisis CCL
- [ ] Backtesting
- [ ] Alertas automáticas
- [ ] Machine Learning

## 📄 Licencia

Este proyecto es de uso educativo y experimental.

---

**Nota**: Los datos de mercado se obtienen mediante yfinance y pueden tener un retraso de 15-20 minutos respecto al tiempo real.
