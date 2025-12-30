# Stock Pro Europe

Plataforma de análisis y predicción de tendencias para las principales bolsas europeas (IBEX 35, DAX 40, CAC 40, etc.).

## Características

- **Dashboard de Mercados**: Vista general de los principales índices europeos con cotizaciones en tiempo real (o diferido según API) y cambios porcentuales.
- **Análisis Técnico**: Gráficos interactivos de precios históricos con indicadores técnicos clave:
  - **RSI (Relative Strength Index)**: Identificación de condiciones de sobrecompra o sobreventa.
  - **SMA (Media Móvil Simple 10)**: Tendencia a corto plazo.
  - **Bandas de Bollinger**: Volatilidad y niveles de soporte/resistencia.
  - **Volatilidad Anualizada**: Medida de riesgo del activo.
- **Predicción de Tendencias**: Utiliza regresión lineal para predecir tendencias futuras basadas en datos históricos.
- **Objetivos de Precio**: Cálculo de rangos de precio esperados basados en volatilidad.

## Stack Tecnológico

### Aplicación Completa
- **SvelteKit** - Framework fullstack con SSR y API routes
- **TypeScript** - Tipado seguro en todo el proyecto
- **TailwindCSS v4** - Estilos modernos y responsivos
- **Chart.js** - Visualización de datos interactiva
- **yahoo-finance2** - Obtención de datos de mercado en tiempo real
- **date-fns** - Manipulación de fechas

## Instalación y Ejecución

### Requisitos previos
- Node.js 18+

### Iniciar la Aplicación

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`.

### Build para Producción

```bash
npm run build
npm run preview
```

## Uso

1. Abre el navegador en `http://localhost:5173`.
2. Revisa el Dashboard para ver el estado general del mercado.
3. Navega a **Analysis**.
4. Introduce un ticker (ej. `TEF.MC` para Telefónica, `SAN.MC` para Santander, `^IBEX` para IBEX 35) y selecciona el periodo.
5. Observa el gráfico de precios con la predicción (línea punteada verde) y los indicadores técnicos.

## Arquitectura

La aplicación utiliza una arquitectura fullstack con SvelteKit:

- **Frontend**: Componentes Svelte con Svelte 5 (runes)
- **Backend**: SvelteKit server-side routes (`+server.ts`)
- **API Routes**:
  - `/api/market-data` - Datos de mercado e información de acciones
  - `/api/predict` - Predicciones de tendencias

Todos los servicios se ejecutan en un único proceso Node.js, simplificando el despliegue y el desarrollo.