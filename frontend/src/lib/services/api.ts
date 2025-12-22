import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface MarketIndex {
    name: string;
    ticker: string;
    symbol?: string; // Mapped from ticker if needed, or use ticker directly
    price: number;
    change: number;
    change_percent: number;
    currency: string;
}

export interface StockDetails {
    ticker: string;
    details: any; // Contains price, currency, change, change_percent
    history: any[];
    prediction: any[];
    kpi?: any;
    targets?: any;
    RSI?: number;
    MA50?: number;
}

export const api = {
    getIndices: async (): Promise<MarketIndex[]> => {
        const response = await axios.get(`${API_URL}/indices`);
        return response.data;
    },
    getStockDetails: async (ticker: string, period = '6mo'): Promise<StockDetails> => {
        const response = await axios.get(`${API_URL}/stock/${ticker}?period=${period}`);
        return response.data;
    },
    getStockPrediction: async (ticker: string, period = '6mo'): Promise<any[]> => {
        const response = await axios.get(`${API_URL}/stock/${ticker}/prediction?period=${period}`);
        return response.data;
    },
    getIndexConstituents: async (ticker: string): Promise<any[]> => {
        const response = await axios.get(`${API_URL}/indices/${encodeURIComponent(ticker)}/constituents`);
        return response.data;
    }
};
