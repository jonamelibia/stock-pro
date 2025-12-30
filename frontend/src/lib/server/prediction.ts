/**
 * Prediction Service
 * Provides time series forecasting using linear regression
 * This replaces the Python Chronos-based prediction service
 */

export interface PredictionResult {
    Date: string;
    PredictedClose: number;
}

export class PredictionService {
    /**
     * Predicts future stock prices using linear regression
     * @param data Array of historical closing prices
     * @param timestamps Array of corresponding timestamps (ISO strings)
     * @param daysAhead Number of days to predict into the future
     * @returns Array of predictions with dates and predicted prices
     */
    static predictTrend(
        data: number[],
        timestamps: string[],
        daysAhead: number = 30
    ): PredictionResult[] {
        if (data.length < 2) {
            return [];
        }

        try {
            // Linear regression: y = mx + b
            const n = data.length;
            const x = Array.from({ length: n }, (_, i) => i);
            const y = data;

            // Calculate slope (m) and intercept (b)
            const sumX = x.reduce((a, b) => a + b, 0);
            const sumY = y.reduce((a, b) => a + b, 0);
            const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
            const sumXX = x.reduce((sum, xi) => sum + xi * xi, 0);

            const m = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
            const b = (sumY - m * sumX) / n;

            // Generate future predictions
            const lastX = x[x.length - 1];
            const lastDate = new Date(timestamps[timestamps.length - 1]);

            const predictions: PredictionResult[] = [];

            for (let i = 1; i <= daysAhead; i++) {
                const futureX = lastX + i;
                const predictedY = m * futureX + b;

                // Calculate future date
                const futureDate = new Date(lastDate);
                futureDate.setDate(futureDate.getDate() + i);

                predictions.push({
                    Date: futureDate.toISOString(),
                    PredictedClose: Math.max(0, predictedY) // Ensure non-negative prices
                });
            }

            return predictions;
        } catch (error) {
            console.error('Prediction error:', error);
            return [];
        }
    }

    /**
     * Alternative prediction method using exponential smoothing
     * Can be used as a fallback or alternative approach
     */
    static predictExponentialSmoothing(
        data: number[],
        timestamps: string[],
        daysAhead: number = 30,
        alpha: number = 0.3
    ): PredictionResult[] {
        if (data.length < 2) {
            return [];
        }

        try {
            // Simple exponential smoothing
            let smoothed = data[0];
            for (let i = 1; i < data.length; i++) {
                smoothed = alpha * data[i] + (1 - alpha) * smoothed;
            }

            // Calculate trend
            const recentData = data.slice(-10);
            const trend = (recentData[recentData.length - 1] - recentData[0]) / recentData.length;

            const lastDate = new Date(timestamps[timestamps.length - 1]);
            const predictions: PredictionResult[] = [];

            for (let i = 1; i <= daysAhead; i++) {
                const predictedValue = smoothed + trend * i;
                const futureDate = new Date(lastDate);
                futureDate.setDate(futureDate.getDate() + i);

                predictions.push({
                    Date: futureDate.toISOString(),
                    PredictedClose: Math.max(0, predictedValue)
                });
            }

            return predictions;
        } catch (error) {
            console.error('Exponential smoothing error:', error);
            return [];
        }
    }
}
