export const ApiService = {
    async getStockInfo(ticker: string) {
        const res = await fetch(`/api/market-data?symbol=${ticker}&type=info`);
        if (!res.ok) {
            throw new Error(`API error: ${res.status}`);
        }
        return res.json();
    },

    async getHistoricalData(ticker: string, period: string = '1mo') {
        const res = await fetch(`/api/market-data?symbol=${ticker}&type=history&period=${period}`);
        if (!res.ok) {
            throw new Error(`API error: ${res.status}`);
        }
        return res.json();
    },

    async getConstituents(indexTicker: string) {
        const res = await fetch(`/api/market-data?symbol=${indexTicker}&type=constituents`);
        return res.json();
    },

    async searchStocks(query: string) {
        try {
            const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            if (!res.ok) {
                throw new Error(`Search API error: ${res.status}`);
            }
            return await res.json();
        } catch (e) {
            console.warn('Search service error:', e);
            return { results: [] };
        }
    },

    async getPrediction(ticker: string, history: any[]) {
        try {
            const data = history.map((h) => h.close);
            const timestamps = history.map((h) => h.date);

            const res = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ticker,
                    data,
                    timestamps,
                    days_ahead: 30
                })
            });

            if (!res.ok) {
                throw new Error(`Prediction API error: ${res.status}`);
            }

            return await res.json();
        } catch (e) {
            console.warn('Prediction service error, using fallback:', e);
            return null;
        }
    }
};

