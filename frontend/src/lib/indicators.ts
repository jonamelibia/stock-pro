export const Indicators = {
    calculateRSI(data: number[], window: number = 14): number[] {
        const rsi = new Array(data.length).fill(null);
        if (data.length <= window) return rsi;

        let gains = 0;
        let losses = 0;

        for (let i = 1; i <= window; i++) {
            const diff = data[i] - data[i - 1];
            if (diff > 0) gains += diff;
            else losses -= diff;
        }

        let avgGain = gains / window;
        let avgLoss = losses / window;
        rsi[window] = 100 - 100 / (1 + avgGain / avgLoss);

        for (let i = window + 1; i < data.length; i++) {
            const diff = data[i] - data[i - 1];
            const gain = diff > 0 ? diff : 0;
            const loss = diff < 0 ? -diff : 0;

            avgGain = (avgGain * (window - 1) + gain) / window;
            avgLoss = (avgLoss * (window - 1) + loss) / window;

            rsi[i] = 100 - 100 / (1 + avgGain / avgLoss);
        }

        return rsi;
    },

    calculateSMA(data: number[], window: number): number[] {
        const sma = new Array(data.length).fill(null);
        for (let i = window - 1; i < data.length; i++) {
            const slice = data.slice(i - window + 1, i + 1);
            const sum = slice.reduce((a, b) => a + b, 0);
            sma[i] = sum / window;
        }
        return sma;
    },

    calculateBollingerBands(data: number[], window: number = 20, stdDev: number = 2) {
        const upper = new Array(data.length).fill(null);
        const lower = new Array(data.length).fill(null);
        const mid = this.calculateSMA(data, window);

        for (let i = window - 1; i < data.length; i++) {
            const slice = data.slice(i - window + 1, i + 1);
            const avg = mid[i] as number;
            const squareDiffs = slice.map((value) => Math.pow(value - avg, 2));
            const variance = squareDiffs.reduce((a, b) => a + b, 0) / window;
            const sd = Math.sqrt(variance);

            upper[i] = avg + stdDev * sd;
            lower[i] = avg - stdDev * sd;
        }

        return { upper, lower, mid };
    },

    calculateVolatility(data: number[]): number {
        if (data.length < 2) return 0;
        const returns = [];
        for (let i = 1; i < data.length; i++) {
            returns.push(Math.log(data[i] / data[i - 1]));
        }
        const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
        const squareDiffs = returns.map((r) => Math.pow(r - mean, 2));
        const variance = squareDiffs.reduce((a, b) => a + b, 0) / (returns.length - 1);
        const vol = Math.sqrt(variance) * Math.sqrt(252); // Annualized
        return isNaN(vol) ? 0 : vol;
    }
};
