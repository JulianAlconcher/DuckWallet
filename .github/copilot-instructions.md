# 🧠 Copilot Instructions – CEDEAR Screener Top 5 Diario

## 1. Propósito General

El objetivo del proyecto es construir una **aplicación informativa** que muestre diariamente un **Top 5 de CEDEARs con mayor fortaleza técnica**, basada en el comportamiento de sus **acciones subyacentes en mercados internacionales**.

⚠️ El sistema **NO realiza recomendaciones financieras**, ni sugiere compra o venta.  
Su fin es **educativo, analítico y experimental**.

---

## 2. Alcance del MVP

- Instrumentos: **CEDEARs operables en Argentina**
- Mercado subyacente: **NASDAQ / NYSE**
- Análisis basado en:
  - Acción subyacente (USD)
  - No en el precio local en ARS
- Frecuencia: **diaria**
- Salida: **Top 5 CEDEARs rankeados**

---

## 3. Definición de “CEDEAR prometedor”

Un CEDEAR se considera prometedor cuando **su acción subyacente muestra fortaleza técnica**, independientemente de:

- Tipo de cambio
- CCL
- Precio local en pesos

El foco está en:
- Momentum
- Tendencia
- Volumen
- Indicadores técnicos clásicos

---

## 4. Universo de Activos

El sistema debe trabajar con un **universo cerrado de acciones subyacentes** que tengan CEDEAR en BYMA.

Ejemplos:
- AAPL
- MSFT
- GOOGL
- AMZN
- TSLA
- META
- NVDA
- KO
- JNJ
- JPM

La lista debe ser:
- Configurable
- Estática en el MVP
- Expandible en el futuro

---

## 5. Indicadores Técnicos Utilizados

Indicadores mínimos a calcular sobre la acción subyacente:

- Variación porcentual diaria
- Volumen actual vs promedio móvil (20–30 días)
- RSI (14)
- Media móvil simple (SMA 20)
- Tendencia reciente (últimos 5–10 días)

Indicadores opcionales (no MVP):
- EMA
- MACD
- Bollinger Bands

---

## 6. Sistema de Scoring

Cada acción recibe un **score técnico explicable**.

Ejemplo base (ajustable):

- +3 → Variación diaria > +2%
- +2 → Volumen > promedio 30 días
- +2 → RSI entre 50 y 70
- +2 → Precio > SMA 20
- +1 → Tendencia alcista reciente

Score máximo: **10**

Los CEDEARs se ordenan según el score de su **acción subyacente**.

---

## 7. Arquitectura Técnica

### Backend
- Lenguaje: **Python**
- Framework: **FastAPI**
- Librerías:
  - pandas
  - numpy
  - ta
  - requests

Responsabilidades:
- Obtener datos de acciones subyacentes
- Calcular indicadores técnicos
- Calcular score
- Mapear acción → CEDEAR
- Exponer endpoint `/top5-cedears`

---

### Frontend
- Framework: **React**
- Build tool: **Vite**
- Estilos: **TailwindCSS**

Vista mínima:
- Símbolo CEDEAR
- Empresa
- Score
- Variación diaria (%)
- RSI
- Tendencia

---

## 8. Fuentes de Datos

Fuentes para datos de acciones subyacentes:

- Alpha Vantage (principal)
- Yahoo Finance (fallback / prototipo)

Datos locales (NO MVP):
- Precio CEDEAR en BYMA
- Ratio de conversión
- CCL

---

## 9. Restricciones Clave

El modelo **NO debe**:

- Recomendar comprar o vender
- Estimar retornos
- Ajustar por tipo de cambio
- Dar asesoramiento financiero

Lenguaje permitido:
- “presenta fortaleza técnica”
- “muestra momentum positivo”
- “según los indicadores analizados”

---

## 10. Evolución Futura (Fuera del MVP)

- Integrar precio local del CEDEAR
- Ajuste por ratio de conversión
- Análisis CCL
- Backtesting
- Machine Learning
- Alertas automáticas

---

## 11. Estilo de Desarrollo

- Código simple y modular
- Priorización de reglas claras
- Explicabilidad antes que complejidad
- Diseño incremental

---

## 12. Formato de Salida Esperado

```json
{
  "date": "YYYY-MM-DD",
  "top5": [
    {
      "cedear": "AAPL",
      "company": "Apple Inc.",
      "score": 8,
      "daily_change_pct": 2.3,
      "volume_ratio": 1.5,
      "rsi": 61,
      "trend": "bullish"
    }
  ]
}
