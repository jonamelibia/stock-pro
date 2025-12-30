import { json } from '@sveltejs/kit';
import { FinnhubService } from '$lib/server/finnhub';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
    const symbol = url.searchParams.get('symbol');

    if (!symbol) {
        return json({ news: [] });
    }

    try {
        // Get news from last 7 days
        const to = new Date().toISOString().split('T')[0];
        const from = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

        const news = await FinnhubService.getCompanyNews(symbol, from, to);
        return json({ news });
    } catch (error) {
        console.error('News API error:', error);
        return json({ news: [] });
    }
};
