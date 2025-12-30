import { json } from '@sveltejs/kit';
import { PredictionService } from '$lib/server/prediction';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
    try {
        const body = await request.json();
        const { ticker, data, timestamps, days_ahead = 30 } = body;

        // Validate input
        if (!ticker || !data || !timestamps) {
            return json(
                { error: 'Missing required fields: ticker, data, timestamps' },
                { status: 400 }
            );
        }

        if (!Array.isArray(data) || !Array.isArray(timestamps)) {
            return json(
                { error: 'Data and timestamps must be arrays' },
                { status: 400 }
            );
        }

        if (data.length !== timestamps.length) {
            return json(
                { error: 'Data and timestamps arrays must have the same length' },
                { status: 400 }
            );
        }

        // Generate predictions
        const predictions = PredictionService.predictTrend(data, timestamps, days_ahead);

        return json({
            ticker,
            predictions
        });
    } catch (error) {
        console.error('Prediction API error:', error);
        return json(
            { error: 'Internal server error during prediction' },
            { status: 500 }
        );
    }
};
