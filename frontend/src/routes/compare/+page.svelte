<script lang="ts">
    import { onMount, tick } from "svelte";
    import { api, type StockDetails } from "$lib/services/api";
    import Chart from "chart.js/auto";
    import { Search, Plus, X, Activity, TrendingUp, Info } from "lucide-svelte";

    // Constants
    const INDICES = [
        { name: "IBEX 35", symbol: "^IBEX" },
        { name: "DAX 40", symbol: "^GDAXI" },
        { name: "CAC 40", symbol: "^FCHI" },
        { name: "FTSE 100", symbol: "^FTSE" },
        { name: "EURO STOXX 50", symbol: "^STOXX50E" },
    ];

    const COLORS = [
        "#000000", // Black
        "#D71921", // Retro Accent (Red)
        "#555555", // Grey
        "#aaaaaa", // Light Grey
        "#333333", // Dark Grey
        "#000000", // Black
    ];

    // State
    let selectedIndex = $state("");
    let constituents: any[] = $state([]);
    let filteredConstituents: any[] = $state([]);
    let tickerSearch = $state("");

    let comparisonList: {
        ticker: string;
        data: StockDetails;
        color: string;
    }[] = $state([]);
    let period = $state("1mo");
    let loading = $state(false);
    let error = $state("");
    let chart: Chart;
    let canvas: HTMLCanvasElement;

    // Derived
    $effect(() => {
        if (!selectedIndex) {
            filteredConstituents = [];
            return;
        }
        filteredConstituents = constituents.filter(
            (c) =>
                c.ticker.toLowerCase().includes(tickerSearch.toLowerCase()) ||
                c.name.toLowerCase().includes(tickerSearch.toLowerCase()),
        );
    });

    // Methods
    async function loadConstituents() {
        if (!selectedIndex) return;
        loading = true;
        try {
            const data = await api.getIndexConstituents(selectedIndex);
            constituents = data || [];
        } catch (e) {
            console.error(e);
            constituents = [];
        } finally {
            loading = false;
        }
    }

    async function addToComparison(ticker: string) {
        if (!ticker || comparisonList.find((c) => c.ticker === ticker)) return;

        loading = true;
        try {
            const data = await api.getStockDetails(ticker, period);
            comparisonList = [
                ...comparisonList,
                {
                    ticker,
                    data,
                    color: COLORS[comparisonList.length % COLORS.length],
                },
            ];
            tickerSearch = ""; // Clear search
        } catch (e) {
            console.error("Error adding to comparison:", e);
            error = "Failed to add stock.";
        } finally {
            loading = false;
        }
    }

    function removeComparison(ticker: string) {
        comparisonList = comparisonList.filter((c) => c.ticker !== ticker);
    }

    async function updatePeriod() {
        loading = true;
        try {
            const promises = comparisonList.map(async (item) => {
                const data = await api.getStockDetails(item.ticker, period);
                return { ...item, data };
            });
            comparisonList = await Promise.all(promises);
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    // Charting
    $effect(() => {
        if (canvas) {
            const ctx = canvas.getContext("2d");
            if (chart) chart.destroy();

            const datasets = comparisonList.map((item) => {
                // Normalize to % change
                const startPrice = item.data.history[0]?.Close || 1;
                const data = item.data.history.map(
                    (d) => ((d.Close - startPrice) / startPrice) * 100,
                );

                return {
                    label: item.ticker,
                    data: data,
                    borderColor: item.color,
                    backgroundColor: "transparent",
                    borderWidth: 2,
                    tension: 0,
                    pointRadius: 0,
                    pointHoverRadius: 4,
                };
            });

            // Labels from first item (assuming similar frequency/market days)
            const labels =
                comparisonList.length > 0
                    ? comparisonList[0].data.history.map((d) =>
                          new Date(d.Date).toLocaleDateString(),
                      )
                    : [];

            chart = new Chart(ctx!, {
                type: "line",
                data: { labels, datasets },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: "index",
                        intersect: false,
                    },
                    plugins: {
                        legend: {
                            position: "top",
                            labels: {
                                color: "#111",
                                font: { family: "Space Mono" },
                            },
                        },
                        tooltip: {
                            mode: "index",
                            intersect: false,
                            backgroundColor: "#111",
                            titleFont: { family: "Space Mono" },
                            bodyFont: { family: "Space Mono" },
                            cornerRadius: 0,
                            callbacks: {
                                label: (context) =>
                                    `${context.dataset.label}: ${context.parsed.y.toFixed(2)}%`,
                            },
                        },
                    },
                    scales: {
                        x: {
                            grid: { display: false, borderColor: "#111" },
                            ticks: {
                                color: "#111",
                                maxTicksLimit: 8,
                                font: { family: "Space Mono" },
                            },
                        },
                        y: {
                            grid: {
                                color: "rgba(0,0,0,0.1)",
                                borderDash: [2, 2],
                                borderColor: "#111",
                            },
                            ticks: {
                                color: "#111",
                                font: { family: "Space Mono" },
                                callback: (v) => v + "%",
                            },
                        },
                    },
                },
            });
        }
        return () => {
            if (chart) chart.destroy();
        };
    });
</script>

<div
    class="h-full bg-retro-surface text-retro-fg min-h-[calc(100vh-64px)] p-6 font-mono"
>
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <h1
            class="text-3xl font-display uppercase tracking-widest mb-8 flex items-center gap-2 border-b border-retro pb-4"
        >
            <Activity class="w-8 h-8 text-retro-accent" />
            Stock Comparison
        </h1>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
            <!-- Sidebar: Search -->
            <div class="md:col-span-3 space-y-4">
                <div class="bg-white border border-retro p-4">
                    <label
                        class="block text-xs font-bold text-retro-fg uppercase mb-2"
                        >Select Index</label
                    >
                    <div class="relative">
                        <select
                            bind:value={selectedIndex}
                            onchange={loadConstituents}
                            class="w-full bg-white border border-retro p-2 text-sm text-retro-fg focus:outline-none focus:border-retro-accent appearance-none rounded-none"
                        >
                            <option value="">START HERE...</option>
                            {#each INDICES as idx}
                                <option value={idx.symbol}>{idx.name}</option>
                            {/each}
                        </select>
                    </div>

                    {#if selectedIndex}
                        <div class="mt-4 animate-in fade-in">
                            <div class="relative mb-2">
                                <LinkIcon
                                    class="absolute left-3 top-2.5 w-4 h-4 text-gray-400"
                                />
                                <input
                                    type="text"
                                    placeholder="FILTER COMPANIES..."
                                    bind:value={tickerSearch}
                                    class="w-full bg-white border border-retro pl-3 pr-3 py-2 text-sm text-retro-fg focus:outline-none focus:border-retro-accent uppercase font-mono"
                                />
                            </div>

                            <div
                                class="max-h-[400px] overflow-y-auto custom-scrollbar space-y-1 mt-4"
                            >
                                {#each filteredConstituents as company}
                                    <button
                                        class="w-full text-left p-2 border border-transparent hover:bg-retro-surface hover:border-retro flex items-center justify-between group transition-colors"
                                        onclick={() =>
                                            addToComparison(company.ticker)}
                                    >
                                        <div>
                                            <span
                                                class="font-bold text-sm block"
                                                >{company.ticker}</span
                                            >
                                            <span
                                                class="text-xs text-gray-500 truncate block max-w-[140px] uppercase"
                                                >{company.name}</span
                                            >
                                        </div>
                                        <Plus
                                            class="w-4 h-4 text-retro-accent opacity-0 group-hover:opacity-100 transition-all"
                                        />
                                    </button>
                                {/each}
                                {#if loading}
                                    <div
                                        class="text-center py-4 text-gray-500 text-xs uppercase animate-pulse"
                                    >
                                        Loading...
                                    </div>
                                {/if}
                            </div>
                        </div>
                    {/if}
                </div>
            </div>

            <!-- Main Content -->
            <div class="md:col-span-9 space-y-6">
                {#if comparisonList.length > 0}
                    <!-- Chart Card -->
                    <div
                        class="bg-white border border-retro p-4 h-[400px] relative"
                    >
                        <div class="absolute top-4 right-4 z-10">
                            <select
                                bind:value={period}
                                onchange={updatePeriod}
                                class="bg-white border border-retro text-xs text-retro-fg px-2 py-1 uppercase cursor-pointer"
                            >
                                <option value="1mo">1 Month</option>
                                <option value="3mo">3 Months</option>
                                <option value="6mo">6 Months</option>
                                <option value="1y">1 Year</option>
                            </select>
                        </div>
                        <canvas bind:this={canvas}></canvas>
                    </div>

                    <!-- Comparison Table -->
                    <div class="bg-white border border-retro overflow-hidden">
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-sm font-mono">
                                <thead
                                    class="bg-retro-surface text-xs uppercase text-retro-fg border-b border-retro"
                                >
                                    <tr>
                                        <th class="px-4 py-3 text-left w-12"
                                            >Color</th
                                        >
                                        <th class="px-4 py-3 text-left"
                                            >Ticker</th
                                        >
                                        <th class="px-4 py-3 text-right"
                                            >Price</th
                                        >
                                        <th class="px-4 py-3 text-right"
                                            >Change</th
                                        >
                                        <th class="px-4 py-3 text-right"
                                            >Mkt Cap</th
                                        >
                                        <th class="px-4 py-3 text-right">P/E</th
                                        >
                                        <th class="px-4 py-3 text-right"
                                            >Yield</th
                                        >
                                        <th class="px-4 py-3 text-right"
                                            >Beta</th
                                        >
                                        <th class="px-4 py-3 text-right">ROE</th
                                        >
                                        <th class="px-4 py-3 text-right"
                                            >Action</th
                                        >
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-retro">
                                    {#each comparisonList as item}
                                        <tr
                                            class="hover:bg-retro-surface transition-colors group"
                                        >
                                            <td class="px-4 py-3">
                                                <div
                                                    class="w-3 h-3 border border-black"
                                                    style="background-color: {item.color}"
                                                ></div>
                                            </td>
                                            <td
                                                class="px-4 py-3 font-bold text-retro-fg text-left"
                                                >{item.ticker}</td
                                            >
                                            <td class="px-4 py-3 text-right">
                                                {item.data.details.price?.toFixed(
                                                    2,
                                                )}{item.data.details.currency}
                                            </td>
                                            <td
                                                class={`px-4 py-3 text-right font-mono ${item.data.details.change >= 0 ? "text-retro-fg" : "text-retro-accent"}`}
                                            >
                                                {item.data.details.change > 0
                                                    ? "+"
                                                    : ""}{item.data.details.change_percent?.toFixed(
                                                    2,
                                                )}%
                                            </td>
                                            <td
                                                class="px-4 py-3 text-right text-gray-600"
                                            >
                                                {item.data.kpi?.marketCap
                                                    ? (
                                                          item.data.kpi
                                                              .marketCap / 1e9
                                                      ).toFixed(1) + "B"
                                                    : "-"}
                                            </td>
                                            <td
                                                class="px-4 py-3 text-right text-gray-600"
                                            >
                                                {item.data.kpi?.trailingPE?.toFixed(
                                                    1,
                                                ) || "-"}
                                            </td>
                                            <td
                                                class="px-4 py-3 text-right text-retro-accent"
                                            >
                                                {item.data.kpi?.dividendYield
                                                    ? (
                                                          item.data.kpi
                                                              .dividendYield *
                                                          100
                                                      ).toFixed(2) + "%"
                                                    : "-"}
                                            </td>
                                            <td
                                                class="px-4 py-3 text-right text-gray-600"
                                            >
                                                {item.data.kpi?.beta?.toFixed(
                                                    2,
                                                ) || "-"}
                                            </td>
                                            <td
                                                class="px-4 py-3 text-right text-blue-600"
                                            >
                                                {item.data.kpi?.returnOnEquity
                                                    ? (
                                                          item.data.kpi
                                                              .returnOnEquity *
                                                          100
                                                      ).toFixed(1) + "%"
                                                    : "-"}
                                            </td>
                                            <td class="px-4 py-3 text-right">
                                                <button
                                                    class="text-gray-400 hover:text-retro-accent p-1"
                                                    onclick={() =>
                                                        removeComparison(
                                                            item.ticker,
                                                        )}
                                                >
                                                    <X class="w-4 h-4" />
                                                </button>
                                            </td>
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </div>
                    </div>
                {:else}
                    <div
                        class="h-[400px] flex flex-col items-center justify-center text-gray-500 border border-dashed border-retro rounded-none bg-white"
                    >
                        <TrendingUp class="w-12 h-12 mb-4 opacity-50" />
                        <p
                            class="text-lg font-display uppercase tracking-wider"
                        >
                            No stocks selected
                        </p>
                        <p class="text-sm font-mono uppercase mt-2">
                            Select an index and add companies to compare
                        </p>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    /* Custom Scrollbar - Retro Style */
    .custom-scrollbar::-webkit-scrollbar {
        width: 8px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background: var(--color-bg);
        border-left: 1px solid var(--color-fg);
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: var(--color-fg);
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
        background: var(--color-accent);
    }
</style>
