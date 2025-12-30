<script lang="ts">
    import {
        TrendingUp,
        TrendingDown,
        BarChart3,
        Newspaper,
        Search,
    } from "lucide-svelte";
    import { goto } from "$app/navigation";
    import StockSearch from "$lib/components/StockSearch.svelte";
    import MarketHeatmap from "$lib/components/MarketHeatmap.svelte";
    import NewsCard from "$lib/components/NewsCard.svelte";

    interface Props {
        data: {
            stocks: any[];
            news: any[];
        };
    }

    let { data }: Props = $props();

    function handleStockSelect(symbol: string) {
        goto(`/analysis?ticker=${symbol}`);
    }

    function viewStock(symbol: string) {
        goto(`/analysis?ticker=${symbol}`);
    }
</script>

<div class="py-8 w-full px-4 md:px-6">
    <div class="space-y-8">
        <!-- Header -->
        <div class="space-y-4">
            <h1 class="text-4xl font-bold text-gray-900">Market Dashboard</h1>
            <p class="text-lg text-gray-600">
                Track popular stocks and market trends in real-time
            </p>
        </div>

        <!-- Search -->
        <div class="w-full">
            <StockSearch onSelect={handleStockSelect} />
        </div>

        <!-- Main Content -->
        <div class="space-y-8">
            <!-- Popular Stocks -->
            <div class="space-y-4">
                <div class="flex items-center justify-between">
                    <h2 class="text-2xl font-bold text-gray-900">
                        Popular Stocks
                    </h2>
                    <a
                        href="/analysis"
                        class="text-sm font-semibold text-blue-600 hover:text-blue-700"
                    >
                        View Analysis →
                    </a>
                </div>

                <div
                    class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
                >
                    {#each data.stocks as stock}
                        <button
                            onclick={() => viewStock(stock.symbol)}
                            class="card p-5 text-left hover:shadow-lg transition-all border border-transparent hover:border-text-secondary group flex flex-col justify-between h-full"
                        >
                            <div class="space-y-4 w-full">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center gap-3">
                                        {#if stock.logo}
                                            <img
                                                src={stock.logo}
                                                alt={stock.symbol}
                                                class="w-8 h-8 rounded-full object-contain bg-white p-0.5 border border-gray-100"
                                            />
                                        {:else}
                                            <div
                                                class="p-2 rounded-full bg-gray-100 group-hover:bg-blue-50 transition-colors"
                                            >
                                                <BarChart3
                                                    class="text-gray-400 group-hover:text-blue-600 transition-colors"
                                                    size={16}
                                                />
                                            </div>
                                        {/if}
                                        <span
                                            class="font-bold text-primary text-lg"
                                            >{stock.symbol}</span
                                        >
                                    </div>
                                </div>

                                <div class="flex items-end justify-between">
                                    <div
                                        class="text-2xl font-bold text-primary"
                                    >
                                        ${stock.price?.toFixed(2)}
                                    </div>

                                    <div
                                        class="px-2.5 py-1 rounded-full text-xs font-bold {stock.change_percent >=
                                        0
                                            ? 'bg-green-100 text-green-700'
                                            : 'bg-red-100 text-red-700'}"
                                    >
                                        {stock.change_percent > 0
                                            ? "+"
                                            : ""}{stock.change_percent?.toFixed(
                                            2,
                                        )}%
                                    </div>
                                </div>
                            </div>
                        </button>
                    {/each}
                </div>
            </div>

            <!-- Market Heatmap -->
            <div class="space-y-4">
                <h2 class="text-2xl font-bold text-gray-900">Market Heatmap</h2>
                <MarketHeatmap stocks={data.stocks} />
            </div>

            <!-- Latest News -->
            <div class="space-y-4">
                <div class="flex items-center gap-2">
                    <Newspaper class="text-blue-600" size={24} />
                    <h2 class="text-2xl font-bold text-gray-900">
                        Latest News
                    </h2>
                </div>
                <NewsCard news={data.news} />
            </div>
        </div>
    </div>
</div>
