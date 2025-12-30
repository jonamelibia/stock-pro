import { FinnhubService } from './finnhub';

export const MarketDataService = {
    /**
     * Get popular/trending stocks
     */
    async getPopularStocks() {
        const popularSymbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'BRK.B', 'JPM', 'V'];

        const results = await Promise.all(
            popularSymbols.map(async (symbol) => {
                try {
                    const [quote, profile] = await Promise.all([
                        FinnhubService.getQuote(symbol),
                        FinnhubService.getCompanyProfile(symbol)
                    ]);

                    if (!quote) return null;

                    return {
                        symbol: symbol,
                        name: profile?.name || symbol,
                        price: quote.c,
                        change: quote.d,
                        change_percent: quote.dp,
                        currency: 'USD',
                        logo: profile?.logo || null
                    };
                } catch (e) {
                    console.error(`Error fetching ${symbol}:`, e);
                    return null;
                }
            })
        );

        return results.filter((r) => r !== null);
    },

    /**
     * Get historical data for a stock
     */
    async getHistoricalData(symbol: string, period: string = '1mo') {
        try {
            // Calculate date range based on period
            const to = Math.floor(Date.now() / 1000);
            let from: number;

            switch (period) {
                case '1d':
                    from = to - 86400;
                    break;
                case '5d':
                    from = to - 86400 * 5;
                    break;
                case '1mo':
                    from = to - 86400 * 30;
                    break;
                case '3mo':
                    from = to - 86400 * 90;
                    break;
                case '6mo':
                    from = to - 86400 * 180;
                    break;
                case '1y':
                    from = to - 86400 * 365;
                    break;
                default:
                    from = to - 86400 * 30;
            }

            const candles = await FinnhubService.getCandles(symbol, 'D', from, to);

            if (!candles || candles.s === 'no_data') {
                return [];
            }

            // Transform to our format
            return candles.t.map((timestamp, index) => ({
                date: new Date(timestamp * 1000).toISOString().split('T')[0],
                open: candles.o[index],
                high: candles.h[index],
                low: candles.l[index],
                close: candles.c[index],
                volume: candles.v[index]
            }));
        } catch (error) {
            console.error('Error fetching historical data:', error);
            return [];
        }
    },

    /**
     * Get stock info including company profile and current quote
     */
    async getStockInfo(symbol: string) {
        try {
            const [profile, quote] = await Promise.all([
                FinnhubService.getCompanyProfile(symbol),
                FinnhubService.getQuote(symbol)
            ]);

            if (!profile || !quote) {
                throw new Error('Could not fetch stock info');
            }

            return {
                symbol: profile.ticker,
                longName: profile.name,
                sector: profile.finnhubIndustry || 'N/A',
                industry: profile.finnhubIndustry || 'N/A',
                description: `${profile.name} is a company listed on ${profile.exchange}. Market Cap: $${(profile.marketCapitalization * 1000000).toLocaleString()}`,
                price: quote.c,
                change: quote.d,
                change_percent: quote.dp,
                marketCap: profile.marketCapitalization * 1000000, // Finnhub returns in millions
                trailingPE: null, // Not available in Finnhub free tier
                beta: null, // Not available in Finnhub free tier
                logo: profile.logo,
                website: profile.weburl,
                country: profile.country,
                currency: profile.currency,
                exchange: profile.exchange,
                ipo: profile.ipo
            };
        } catch (error) {
            console.error('Error fetching stock info:', error);
            throw error;
        }
    },

    /**
     * Search for stocks
     */
    async searchStocks(query: string) {
        try {
            const results = await FinnhubService.searchSymbols(query);

            return results.map((result) => ({
                symbol: result.symbol,
                name: result.description,
                type: result.type,
                region: 'US', // Finnhub doesn't provide region in search
                currency: 'USD',
                matchScore: '1.0'
            }));
        } catch (error) {
            console.error('Error searching stocks:', error);
            return [];
        }
    }
};
