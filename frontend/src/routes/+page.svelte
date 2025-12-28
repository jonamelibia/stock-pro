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

<div class="min-h-screen relative overflow-hidden bg-retro-surface">
    <!-- Ticker Tape -->
    <div
        class="relative z-10 w-full bg-retro-surface border-b border-retro py-2 overflow-hidden flex"
    >
        <div class="flex animate-marquee whitespace-nowrap gap-8 items-center">
            {#each [...indices, ...indices] as index}
                <div class="flex items-center gap-2 font-mono text-sm">
                    <span class="font-bold uppercase tracking-wide"
                        >{index.name}</span
                    >
                    <span
                        class={` ${index.change >= 0 ? "text-retro-fg" : "text-retro-accent"}`}
                    >
                        {index.price.toFixed(2)}
                    </span>
                    <span
                        class={`text-xs ${index.change >= 0 ? "text-retro-fg" : "text-retro-accent"}`}
                    >
                        {index.change >= 0 ? "▲" : "▼"}
                        {Math.abs(index.change_percent)}%
                    </span>
                </div>
            {/each}
            {#if indices.length === 0}
                <span class="text-retro-fg font-mono text-sm uppercase"
                    >Loading Market Data...</span
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
            class="inline-flex items-center gap-2 px-3 py-1 border border-retro text-retro-fg text-xs font-mono uppercase mb-8 fade-in-up"
        >
            <span class="relative flex h-2 w-2">
                <span
                    class="animate-ping absolute inline-flex h-full w-full rounded-full bg-retro-accent opacity-75"
                ></span>
                <span
                    class="relative inline-flex rounded-full h-2 w-2 bg-retro-accent"
                ></span>
            </span>
            Powered by Amazon Chronos AI
        </div>

        <!-- Hero Title -->
        <h1
            class="text-5xl md:text-7xl font-display mb-6 fade-in-up delay-100 uppercase leading-none"
        >
            <span class="block">Predict the Market.</span>
            <span class="text-retro-accent">Own the Future.</span>
        </h1>

        <!-- Hero Subtitle -->
        <p
            class="text-xl text-retro-fg font-mono max-w-2xl mb-10 fade-in-up delay-200 uppercase tracking-tight"
        >
            Advanced neural forecasting models meet real-time european market
            data.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 mb-20 fade-in-up delay-300">
            <a
                href="/analysis"
                class="group relative px-8 py-4 border border-retro bg-retro-accent text-white font-mono uppercase text-lg hover:bg-white hover:text-retro-accent transition-colors"
            >
                <span class="relative z-10 flex items-center gap-2">
                    Launch Platform <ArrowRight
                        class="w-5 h-5 group-hover:translate-x-1 transition-transform"
                    />
                </span>
            </a>
        </div>

        <!-- Feature Grid -->
        <div
            class="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl fade-in-up delay-500"
        >
            <!-- Feature 1 -->
            <div
                class="p-8 border border-retro bg-retro-surface hover:bg-white transition-colors text-left group"
            >
                <div
                    class="border border-retro w-12 h-12 flex items-center justify-center mb-4 text-retro-fg group-hover:bg-retro-accent group-hover:text-white group-hover:border-retro-accent transition-colors"
                >
                    <TrendingUp class="w-6 h-6" />
                </div>
                <h3 class="text-xl font-display uppercase mb-2">
                    AI-Driven Forecasts
                </h3>
                <p class="text-retro-fg font-mono text-sm leading-relaxed">
                    Leveraging state-of-the-art Chronos Transformers to predict
                    short-term price movements.
                </p>
            </div>

            <!-- Feature 2 -->
            <div
                class="p-8 border border-retro bg-retro-surface hover:bg-white transition-colors text-left group"
            >
                <div
                    class="border border-retro w-12 h-12 flex items-center justify-center mb-4 text-retro-fg group-hover:bg-retro-accent group-hover:text-white group-hover:border-retro-accent transition-colors"
                >
                    <Activity class="w-6 h-6" />
                </div>
                <h3 class="text-xl font-display uppercase mb-2">
                    Technical Indicators
                </h3>
                <p class="text-retro-fg font-mono text-sm leading-relaxed">
                    Automated calculation of Bollinger Bands, RSI, MACD, and
                    Moving Averages.
                </p>
            </div>

            <!-- Feature 3 -->
            <div
                class="p-8 border border-retro bg-retro-surface hover:bg-white transition-colors text-left group"
            >
                <div
                    class="border border-retro w-12 h-12 flex items-center justify-center mb-4 text-retro-fg group-hover:bg-retro-accent group-hover:text-white group-hover:border-retro-accent transition-colors"
                >
                    <BarChart2 class="w-6 h-6" />
                </div>
                <h3 class="text-xl font-display uppercase mb-2">
                    Market Constituents
                </h3>
                <p class="text-retro-fg font-mono text-sm leading-relaxed">
                    Drill down into major European indices (IBEX, DAX, CAC) to
                    find top performers.
                </p>
            </div>
        </div>

        <footer
            class="mt-20 text-retro-fg font-mono text-xs uppercase border-t border-retro pt-8 w-full max-w-6xl"
        >
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
