import { MarketDataService } from '$lib/server/marketData';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
    const stocks = await MarketDataService.getPopularStocks();
    return {
        stocks
    };
};

