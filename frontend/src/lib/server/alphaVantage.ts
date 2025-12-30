/**
 * Alpha Vantage API Service
 * Provides stock market data from Alpha Vantage API
 */

import { env } from '$env/dynamic/private';

const ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query';

// Get API key from environment variable
function getApiKey(): string {
    const apiKey = env.ALPHA_VANTAGE_API_KEY;
    if (!apiKey) {
        throw new Error('ALPHA_VANTAGE_API_KEY environment variable is not set');
    }
    return apiKey;
}

export interface SearchResult {
    symbol: string;
    name: string;
    type: string;
    region: string;
    marketOpen: string;
    marketClose: string;
    timezone: string;
    currency: string;
    matchScore: string;
}

export interface Quote {
    symbol: string;
    price: number;
    change: number;
    changePercent: number;
    volume: number;
    latestTradingDay: string;
    previousClose: number;
    open: number;
    high: number;
    low: number;
}

export interface HistoricalDataPoint {
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
}

export interface CompanyOverview {
    symbol: string;
    name: string;
    description: string;
    sector: string;
    industry: string;
    marketCap: number;
    peRatio: number;
    dividendYield: number;
    beta: number;
    fiftyTwoWeekHigh: number;
    fiftyTwoWeekLow: number;
}

export const AlphaVantageService = {
    /**
     * Search for stock symbols by keywords
     */
    async searchSymbols(keywords: string): Promise<SearchResult[]> {
        try {
            const apiKey = getApiKey();
            const url = `${ALPHA_VANTAGE_BASE_URL}?function=SYMBOL_SEARCH&keywords=${encodeURIComponent(keywords)}&apikey=${apiKey}`;

            const response = await fetch(url);
            const data = await response.json();

            if (data['Error Message']) {
                throw new Error(data['Error Message']);
            }

            if (data['Note']) {
                // API rate limit reached
                console.warn('Alpha Vantage API rate limit reached');
                return [];
            }

            const matches = data['bestMatches'] || [];
            return matches.map((match: any) => ({
                symbol: match['1. symbol'],
                name: match['2. name'],
                type: match['3. type'],
                region: match['4. region'],
                marketOpen: match['5. marketOpen'],
                marketClose: match['6. marketClose'],
                timezone: match['7. timezone'],
                currency: match['8. currency'],
                matchScore: match['9. matchScore']
            }));
        } catch (error) {
            console.error('Error searching symbols:', error);
            return [];
        }
    },

    /**
     * Get current quote for a symbol
     */
    async getQuote(symbol: string): Promise<Quote | null> {
        try {
            const apiKey = getApiKey();
            const url = `${ALPHA_VANTAGE_BASE_URL}?function=GLOBAL_QUOTE&symbol=${encodeURIComponent(symbol)}&apikey=${apiKey}`;

            const response = await fetch(url);
            const data = await response.json();

            if (data['Error Message']) {
                throw new Error(data['Error Message']);
            }

            if (data['Note']) {
                console.warn('Alpha Vantage API rate limit reached');
                return null;
            }

            const quote = data['Global Quote'];
            if (!quote || Object.keys(quote).length === 0) {
                return null;
            }

            return {
                symbol: quote['01. symbol'],
                price: parseFloat(quote['05. price']),
                change: parseFloat(quote['09. change']),
                changePercent: parseFloat(quote['10. change percent'].replace('%', '')),
                volume: parseInt(quote['06. volume']),
                latestTradingDay: quote['07. latest trading day'],
                previousClose: parseFloat(quote['08. previous close']),
                open: parseFloat(quote['02. open']),
                high: parseFloat(quote['03. high']),
                low: parseFloat(quote['04. low'])
            };
        } catch (error) {
            console.error('Error fetching quote:', error);
            return null;
        }
    },

    /**
     * Get daily historical data for a symbol
     */
    async getHistoricalData(symbol: string, outputSize: 'compact' | 'full' = 'compact'): Promise<HistoricalDataPoint[]> {
        try {
            const apiKey = getApiKey();
            const url = `${ALPHA_VANTAGE_BASE_URL}?function=TIME_SERIES_DAILY&symbol=${encodeURIComponent(symbol)}&outputsize=${outputSize}&apikey=${apiKey}`;

            const response = await fetch(url);
            const data = await response.json();

            if (data['Error Message']) {
                throw new Error(data['Error Message']);
            }

            if (data['Note']) {
                console.warn('Alpha Vantage API rate limit reached');
                return [];
            }

            const timeSeries = data['Time Series (Daily)'];
            if (!timeSeries) {
                return [];
            }

            const historicalData: HistoricalDataPoint[] = [];
            for (const [date, values] of Object.entries(timeSeries)) {
                const dayData: any = values;
                historicalData.push({
                    date,
                    open: parseFloat(dayData['1. open']),
                    high: parseFloat(dayData['2. high']),
                    low: parseFloat(dayData['3. low']),
                    close: parseFloat(dayData['4. close']),
                    volume: parseInt(dayData['5. volume'])
                });
            }

            // Sort by date ascending
            return historicalData.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
        } catch (error) {
            console.error('Error fetching historical data:', error);
            return [];
        }
    },

    /**
     * Get company overview/fundamental data
     */
    async getCompanyOverview(symbol: string): Promise<CompanyOverview | null> {
        try {
            const apiKey = getApiKey();
            const url = `${ALPHA_VANTAGE_BASE_URL}?function=OVERVIEW&symbol=${encodeURIComponent(symbol)}&apikey=${apiKey}`;

            const response = await fetch(url);
            const data = await response.json();

            if (data['Error Message']) {
                throw new Error(data['Error Message']);
            }

            if (data['Note']) {
                console.warn('Alpha Vantage API rate limit reached');
                return null;
            }

            if (!data['Symbol']) {
                return null;
            }

            return {
                symbol: data['Symbol'],
                name: data['Name'],
                description: data['Description'] || 'No description available',
                sector: data['Sector'] || 'N/A',
                industry: data['Industry'] || 'N/A',
                marketCap: parseInt(data['MarketCapitalization']) || 0,
                peRatio: parseFloat(data['PERatio']) || 0,
                dividendYield: parseFloat(data['DividendYield']) || 0,
                beta: parseFloat(data['Beta']) || 0,
                fiftyTwoWeekHigh: parseFloat(data['52WeekHigh']) || 0,
                fiftyTwoWeekLow: parseFloat(data['52WeekLow']) || 0
            };
        } catch (error) {
            console.error('Error fetching company overview:', error);
            return null;
        }
    }
};
