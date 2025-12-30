import type { PageServerLoad } from './$types';
import { MarketDataService } from '$lib/server/marketData';
import { FinnhubService } from '$lib/server/finnhub';

export const load: PageServerLoad = async () => {
    try {
        const stocks = await MarketDataService.getPopularStocks();

        // Get news for top stocks
        const to = new Date().toISOString().split('T')[0];
        const from = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

        // Get news for first 3 stocks
        const newsPromises = stocks.slice(0, 3).map(stock =>
            FinnhubService.getCompanyNews(stock.symbol, from, to)
        );

        const newsResults = await Promise.all(newsPromises);

        // Flatten and remove duplicates by ID
        const newsMap = new Map();
        newsResults.flat().forEach(item => {
            if (!newsMap.has(item.id)) {
                newsMap.set(item.id, item);
            }
        });

        const allNews = Array.from(newsMap.values())
            .sort((a, b) => b.datetime - a.datetime)
            .slice(0, 30);

        return { stocks, news: allNews };
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        return { stocks: [], news: [] };
    }
};
