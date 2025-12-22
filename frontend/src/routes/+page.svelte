<script lang="ts">
    import { onMount } from "svelte";
    import { api, type MarketIndex } from "$lib/services/api";
    import { ArrowRight, TrendingUp, Activity, BarChart2 } from "lucide-svelte";

    let indices: MarketIndex[] = $state([]);
    let loaded = $state(false);

    onMount(async () => {
        try {
            const allIndices = await api.getIndices();
            // Filter for European Indices only
            const europeanSymbols = [
                "^IBEX",
                "^GDAXI",
                "^FCHI",
                "^FTSE",
                "^STOXX50E",
            ];
            indices = allIndices.filter((i) =>
                europeanSymbols.includes(i.ticker),
            );
            loaded = true;
        } catch (e) {
            console.error("Failed to load indices for ticker", e);
        }
    });
</script>

<div class="min-h-screen bg-slate-900 text-white overflow-hidden relative">
    <!-- Background Effects -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
        <div
            class="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-blue-600 rounded-full blur-[128px] opacity-20 animate-pulse"
        ></div>
        <div
            class="absolute bottom-[-10%] left-[-5%] w-[500px] h-[500px] bg-purple-600 rounded-full blur-[128px] opacity-20 animate-pulse delay-1000"
        ></div>
    </div>

    <!-- Ticker Tape -->
    <div
        class="relative z-10 w-full bg-black/30 backdrop-blur-sm border-b border-white/5 py-2 overflow-hidden flex"
    >
        <div class="flex animate-marquee whitespace-nowrap gap-8 items-center">
            {#each [...indices, ...indices] as index}
                <div class="flex items-center gap-2">
                    <span class="font-bold text-gray-400">{index.name}</span>
                    <span
                        class={`font-mono font-medium ${index.change >= 0 ? "text-green-400" : "text-red-400"}`}
                    >
                        {index.price.toFixed(2)}
                    </span>
                    <span
                        class={`text-xs ${index.change >= 0 ? "text-green-500" : "text-red-500"}`}
                    >
                        {index.change >= 0 ? "▲" : "▼"}
                        {Math.abs(index.change_percent)}%
                    </span>
                </div>
            {/each}
            {#if indices.length === 0}
                <span class="text-gray-500 text-sm">Loading Market Data...</span
                >
            {/if}
        </div>
    </div>

    <!-- Main Content -->
    <main
        class="relative z-10 container mx-auto px-4 pt-20 pb-12 flex flex-col items-center text-center"
    >
        <!-- Hero Badge -->
        <div
            class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-8 fade-in-up"
        >
            <span class="relative flex h-2 w-2">
                <span
                    class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"
                ></span>
                <span
                    class="relative inline-flex rounded-full h-2 w-2 bg-blue-500"
                ></span>
            </span>
            Powered by Amazon Chronos AI
        </div>

        <!-- Hero Title -->
        <h1
            class="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 fade-in-up delay-100"
        >
            <span
                class="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400"
            >
                Predict the Market.
            </span>
            <br />
            <span class="text-white">Own the Future.</span>
        </h1>

        <!-- Hero Subtitle -->
        <p class="text-xl text-slate-400 max-w-2xl mb-10 fade-in-up delay-200">
            Advanced neural forecasting models meet real-time european market
            data. Visualize trends, analyze volatility, and spot opportunities
            before they happen.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 mb-20 fade-in-up delay-300">
            <a
                href="/analysis"
                class="group relative px-8 py-4 bg-blue-600 rounded-lg font-bold text-lg overflow-hidden transition-all hover:scale-105 hover:shadow-[0_0_20px_rgba(37,99,235,0.5)]"
            >
                <span class="relative z-10 flex items-center gap-2">
                    Launch Platform <ArrowRight
                        class="w-5 h-5 group-hover:translate-x-1 transition-transform"
                    />
                </span>
                <div
                    class="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 opacity-0 group-hover:opacity-100 transition-opacity"
                ></div>
            </a>
        </div>

        <!-- Feature Grid -->
        <div
            class="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl fade-in-up delay-500"
        >
            <!-- Feature 1 -->
            <div
                class="p-8 rounded-2xl bg-slate-800/50 backdrop-blur border border-white/5 hover:border-blue-500/30 transition-all hover:-translate-y-1"
            >
                <div
                    class="w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center mb-4 text-blue-400"
                >
                    <TrendingUp class="w-6 h-6" />
                </div>
                <h3 class="text-xl font-bold mb-2">AI-Driven Forecasts</h3>
                <p class="text-slate-400">
                    Leveraging state-of-the-art Chronos Transformers to predict
                    short-term price movements with high accuracy.
                </p>
            </div>

            <!-- Feature 2 -->
            <div
                class="p-8 rounded-2xl bg-slate-800/50 backdrop-blur border border-white/5 hover:border-purple-500/30 transition-all hover:-translate-y-1"
            >
                <div
                    class="w-12 h-12 rounded-lg bg-purple-500/20 flex items-center justify-center mb-4 text-purple-400"
                >
                    <Activity class="w-6 h-6" />
                </div>
                <h3 class="text-xl font-bold mb-2">Technical Indicators</h3>
                <p class="text-slate-400">
                    Automated calculation of Bollinger Bands, RSI, MACD, and
                    Moving Averages for deep technical analysis.
                </p>
            </div>

            <!-- Feature 3 -->
            <div
                class="p-8 rounded-2xl bg-slate-800/50 backdrop-blur border border-white/5 hover:border-cyan-500/30 transition-all hover:-translate-y-1"
            >
                <div
                    class="w-12 h-12 rounded-lg bg-cyan-500/20 flex items-center justify-center mb-4 text-cyan-400"
                >
                    <BarChart2 class="w-6 h-6" />
                </div>
                <h3 class="text-xl font-bold mb-2">Market Constituents</h3>
                <p class="text-slate-400">
                    Drill down into major European indices (IBEX, DAX, CAC) to
                    find the top performers and hidden gems.
                </p>
            </div>
        </div>

        <footer class="mt-20 text-slate-500 text-sm">
            © 2025 Stock Pro Europe. Data provided for demonstration purposes.
        </footer>
    </main>
</div>

<style>
    @keyframes marquee {
        0% {
            transform: translateX(0);
        }
        100% {
            transform: translateX(-50%);
        }
    }
    .animate-marquee {
        animation: marquee 30s linear infinite;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .fade-in-up {
        animation: fadeInUp 0.8s ease-out forwards;
        opacity: 0;
    }
    .delay-100 {
        animation-delay: 0.1s;
    }
    .delay-200 {
        animation-delay: 0.2s;
    }
    .delay-300 {
        animation-delay: 0.3s;
    }
    .delay-500 {
        animation-delay: 0.5s;
    }
</style>
