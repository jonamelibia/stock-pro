import { env } from '$env/dynamic/private';

const FINNHUB_BASE_URL = 'https://finnhub.io/api/v1';

function getApiKey(): string {
    const apiKey = env.FINNHUB_API_KEY;
    if (!apiKey) {
        throw new Error('FINNHUB_API_KEY is not set in environment variables');
    }
    return apiKey;
}

export interface SearchResult {
    symbol: string;
    description: string;
    type: string;
    displaySymbol: string;
}

export interface Quote {
    c: number; // Current price
    d: number; // Change
    dp: number; // Percent change
    h: number; // High price of the day
    l: number; // Low price of the day
    o: number; // Open price of the day
    pc: number; // Previous close price
    t: number; // Timestamp
}

export interface CompanyProfile {
    country: string;
    currency: string;
    exchange: string;
    ipo: string;
    marketCapitalization: number;
    name: string;
    phone: string;
    shareOutstanding: number;
    ticker: string;
    weburl: string;
    logo: string;
    finnhubIndustry: string;
}

export interface Candle {
    c: number[]; // Close prices
    h: number[]; // High prices
    l: number[]; // Low prices
    o: number[]; // Open prices
    t: number[]; // Timestamps
    v: number[]; // Volumes
    s: string; // Status
}

export const FinnhubService = {
    /**
     * Search for stock symbols
     */
    async searchSymbols(query: string): Promise<SearchResult[]> {
        try {
            const apiKey = getApiKey();
            const url = `${FINNHUB_BASE_URL}/search?q=${encodeURIComponent(query)}&token=${apiKey}`;

            const response = await fetch(url);
            const data = await response.json();

            if (data.error) {
                console.error('Finnhub API error:', data.error);
                return [];
            }

            return data.result || [];
        } catch (error) {
            console.error('Error searching symbols:', error);
            return [];
        }
    },

    /**
     * Get real-time quote for a symbol
     */
    async getQuote(symbol: string): Promise<Quote | null> {
        try {
            const apiKey = getApiKey();
            const url = `${FINNHUB_BASE_URL}/quote?symbol=${encodeURIComponent(symbol)}&token=${apiKey}`;

            const response = await fetch(url);
            const data = await response.json();

            if (data.error || data.c === 0) {
                return null;
            }

            return data;
        } catch (error) {
            console.error('Error getting quote:', error);
            return null;
        }
    },

    /**
     * Get company profile
     */
    async getCompanyProfile(symbol: string): Promise<CompanyProfile | null> {
        try {
            const apiKey = getApiKey();
            const url = `${FINNHUB_BASE_URL}/stock/profile2?symbol=${encodeURIComponent(symbol)}&token=${apiKey}`;

            const response = await fetch(url);
            const data = await response.json();

            if (data.error || !data.ticker) {
                return null;
            }

            return data;
        } catch (error) {
            console.error('Error getting company profile:', error);
            return null;
        }
    },

    /**
     * Get historical candle data
     */
    async getCandles(
        symbol: string,
        resolution: 'D' | 'W' | 'M' = 'D',
        from: number,
        to: number
    ): Promise<Candle | null> {
        try {
            const apiKey = getApiKey();
            const url = `${FINNHUB_BASE_URL}/stock/candle?symbol=${encodeURIComponent(symbol)}&resolution=${resolution}&from=${from}&to=${to}&token=${apiKey}`;

            const response = await fetch(url);
            const data = await response.json();

            if (data.s === 'no_data' || data.error) {
                return null;
            }

            return data;
        } catch (error) {
            console.error('Error getting candles:', error);
            return null;
        }
    },

    /**
     * Get company news
     */
    async getCompanyNews(symbol: string, from: string, to: string): Promise<any[]> {
        try {
            const apiKey = getApiKey();
            const url = `${FINNHUB_BASE_URL}/company-news?symbol=${encodeURIComponent(symbol)}&from=${from}&to=${to}&token=${apiKey}`;

            const response = await fetch(url);
            const data = await response.json();

            if (data.error) {
                return [];
            }

            return data || [];
        } catch (error) {
            console.error('Error getting company news:', error);
            return [];
        }
    }
};
