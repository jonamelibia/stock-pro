import { json } from '@sveltejs/kit';
import { MarketDataService } from '$lib/server/marketData';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
    const query = url.searchParams.get('q');

    if (!query) {
        return json({ results: [] });
    }

    try {
        const results = await MarketDataService.searchStocks(query);
        return json({ results });
    } catch (error) {
        console.error('Search API error:', error);
        return json({ results: [] });
    }
};
