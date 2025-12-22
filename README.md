# Stock Pro Europe

Plataforma de análisis y predicción de tendencias para las principales bolsas europeas (IBEX 35, DAX 40, CAC 40, etc.).

## Características

- **Dashboard de Mercados**: Vista general de los principales índices europeos con cotizaciones en tiempo real (o diferido según API) y cambios porcentuales.
- **Análisis Técnico**: Gráficos interactivos de precios históricos con indicadores técnicos clave:
  - **RSI (Relative Strength Index)**: Identificación de condiciones de sobrecompra o sobreventa.
  - **SMA (Media Móvil Simple 50)**: Tendencia a medio plazo.
  - **EMA (Media Móvil Exponencial 20)**: Tendencia a corto plazo con mayor peso en precios recientes.
  - **MACD**: Convergencia/Divergencia de medias móviles.
- **Predicción AI Avanzada**: Utiliza **Google TimesFM (Time Series Foundation Model)**, un modelo Transformer de 200M parámetros pre-entrenado, para predecir tendencias con alta precisión.

## Stack Tecnológico

### Backend
- **Python** con **FastAPI**.
- **Pandas** & **NumPy** para análisis de datos.
- **Scikit-Learn** para algoritmos de predicción.
- **yfinance** para obtención de datos de mercado.

### Frontend
- **SvelteKit** (Framework fullstack sobre Svelte).
- **TypeScript** para tipado seguro.
- **TailwindCSS** v4 para estilos modernos y responsivos.
- **Chart.js** para visualización de datos.

## Instalación y Ejecución

### Requisitos previos
- Python 3.9+
- Node.js 18+

### 1. Iniciar el Backend

**Nota**: Se recomienda usar **Python 3.9** o **Python 3.10** debido a dependencias de Torch/TimesFM.

```bash
cd backend
# Crear entorno virtual con Python 3.9
/path/to/python3.9 -m venv venv 
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload
```

El backend estará disponible en `http://localhost:8000`.

### 2. Iniciar el Frontend

```bash
cd frontend
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`.

## Uso

1. Abre el navegador en `http://localhost:5173`.
2. Revisa el Dashboard para ver el estado general del mercado.
3. Navega a **Analysis**.
4. Introduce un ticker (ej. `TEF.MC` para Telefónica, `SAN.MC` para Santander, `^IBEX` para IBEX 35) y selecciona el periodo.
5. Observa el gráfico de precios con la predicción (línea punteada verde) y los indicadores técnicos.