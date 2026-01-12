# DuckWallet – CEDEAR Screener Top 5 Diario

DuckWallet es una aplicación informativa que muestra diariamente el Top 5 de CEDEARs con mayor fortaleza técnica, basada en el análisis de sus acciones subyacentes en mercados internacionales (NASDAQ/NYSE).

## Características principales
- Ranking diario de los 5 CEDEARs más fuertes técnicamente
- Análisis basado en indicadores técnicos clásicos (variación diaria, volumen, RSI, SMA, tendencia)
- Backend en **Python** (FastAPI)
- Frontend en **React** + **Vite** + **TailwindCSS**
- Datos obtenidos de Alpha Vantage o Yahoo Finance

## Uso
1. Ejecuta el backend para exponer el endpoint `/top5-cedears`.
2. Inicia el frontend para visualizar el ranking y detalles de cada CEDEAR.

## Importante
- El sistema **no recomienda comprar/vender** ni da asesoramiento financiero.
- El objetivo es educativo y analítico.

## Estructura
- `backend/`: API, lógica de scoring y análisis técnico
- `frontend/`: Interfaz de usuario

---

Desarrollado con fines educativos y experimentales. Para más detalles, consulta la documentación interna del proyecto.