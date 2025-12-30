import { json } from '@sveltejs/kit';
import { MarketDataService } from '$lib/server/marketData';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
    const type = url.searchParams.get('type');
    const symbol = url.searchParams.get('symbol');
    const period = url.searchParams.get('period') || '1mo';

    try {
        switch (type) {
            case 'popular':
                const stocks = await MarketDataService.getPopularStocks();
                return json(stocks);

            case 'info':
                if (!symbol) {
                    return json({ error: 'Symbol required' }, { status: 400 });
                }
                const info = await MarketDataService.getStockInfo(symbol);
                return json(info);

            case 'history':
                if (!symbol) {
                    return json({ error: 'Symbol required' }, { status: 400 });
                }
                const history = await MarketDataService.getHistoricalData(symbol, period);
                return json(history);

            default:
                return json({ error: 'Invalid type' }, { status: 400 });
        }
    } catch (error) {
        console.error('Market data API error:', error);
        return json({ error: 'Failed to fetch data' }, { status: 500 });
    }
};
