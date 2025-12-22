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
        "#3b82f6", // Blue
        "#ef4444", // Red
        "#10b981", // Emerald
        "#f59e0b", // Amber
        "#8b5cf6", // Violet
        "#ec4899", // Pink
        "#06b6d4", // Cyan
        "#f97316", // Orange
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
                    tension: 0.4,
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
                            labels: { color: "#94a3b8" },
                        },
                        tooltip: {
                            mode: "index",
                            intersect: false,
                            callbacks: {
                                label: (context) =>
                                    `${context.dataset.label}: ${context.parsed.y.toFixed(2)}%`,
                            },
                        },
                    },
                    scales: {
                        x: {
                            grid: { color: "rgba(255,255,255,0.05)" },
                            ticks: { color: "#94a3b8", maxTicksLimit: 8 },
                        },
                        y: {
                            grid: { color: "rgba(255,255,255,0.05)" },
                            ticks: {
                                color: "#94a3b8",
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

<div class="h-full bg-slate-900 text-white min-h-[calc(100vh-64px)] p-6">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <h1 class="text-3xl font-bold mb-8 flex items-center gap-2">
            <Activity class="w-8 h-8 text-blue-500" />
            Stock Comparison
        </h1>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
            <!-- Sidebar: Search -->
            <div class="md:col-span-3 space-y-4">
                <div
                    class="bg-slate-800/50 rounded-xl p-4 border border-white/5"
                >
                    <label
                        class="block text-xs font-bold text-slate-400 uppercase mb-2"
                        >Select Index</label
                    >
                    <div class="relative">
                        <select
                            bind:value={selectedIndex}
                            onchange={loadConstituents}
                            class="w-full bg-slate-900 border border-white/10 rounded-lg p-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500 appearance-none"
                        >
                            <option value="">Start here...</option>
                            {#each INDICES as idx}
                                <option value={idx.symbol}>{idx.name}</option>
                            {/each}
                        </select>
                    </div>

                    {#if selectedIndex}
                        <div class="mt-4 animate-in fade-in">
                            <div class="relative mb-2">
                                <Search
                                    class="absolute left-3 top-2.5 w-4 h-4 text-slate-500"
                                />
                                <input
                                    type="text"
                                    placeholder="Filter companies..."
                                    bind:value={tickerSearch}
                                    class="w-full bg-slate-900 border border-white/10 rounded-lg pl-9 pr-3 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                                />
                            </div>

                            <div
                                class="max-h-[400px] overflow-y-auto custom-scrollbar space-y-1"
                            >
                                {#each filteredConstituents as company}
                                    <button
                                        class="w-full text-left p-2 rounded hover:bg-white/5 flex items-center justify-between group transition-colors"
                                        onclick={() =>
                                            addToComparison(company.ticker)}
                                    >
                                        <div>
                                            <span
                                                class="font-bold text-sm block"
                                                >{company.ticker}</span
                                            >
                                            <span
                                                class="text-xs text-slate-500 truncate block max-w-[140px]"
                                                >{company.name}</span
                                            >
                                        </div>
                                        <Plus
                                            class="w-4 h-4 text-slate-500 group-hover:text-blue-400 opacity-0 group-hover:opacity-100 transition-all"
                                        />
                                    </button>
                                {/each}
                                {#if loading}
                                    <div
                                        class="text-center py-4 text-slate-500 text-xs"
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
                        class="bg-slate-800/30 rounded-xl border border-white/5 p-4 h-[400px] relative"
                    >
                        <div class="absolute top-4 right-4 z-10">
                            <select
                                bind:value={period}
                                onchange={updatePeriod}
                                class="bg-slate-900 border border-white/10 text-xs text-white rounded px-2 py-1"
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
                    <div
                        class="bg-slate-800/30 rounded-xl border border-white/5 overflow-hidden"
                    >
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-sm">
                                <thead
                                    class="bg-slate-900/50 text-xs uppercase text-slate-500 text-right"
                                >
                                    <tr>
                                        <th class="px-4 py-3 text-left w-12"
                                            >Color</th
                                        >
                                        <th class="px-4 py-3 text-left"
                                            >Ticker</th
                                        >
                                        <th class="px-4 py-3">Price</th>
                                        <th class="px-4 py-3">Change</th>
                                        <th class="px-4 py-3">Mkt Cap</th>
                                        <th class="px-4 py-3">P/E</th>
                                        <th class="px-4 py-3">Yield</th>
                                        <th class="px-4 py-3">Beta</th>
                                        <th class="px-4 py-3">ROE</th>
                                        <th class="px-4 py-3">Action</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-white/5">
                                    {#each comparisonList as item}
                                        <tr
                                            class="hover:bg-white/5 transition-colors group"
                                        >
                                            <td class="px-4 py-3">
                                                <div
                                                    class="w-3 h-3 rounded-full"
                                                    style="background-color: {item.color}"
                                                ></div>
                                            </td>
                                            <td
                                                class="px-4 py-3 font-bold text-white text-left"
                                                >{item.ticker}</td
                                            >
                                            <td class="px-4 py-3 text-right">
                                                {item.data.details.price?.toFixed(
                                                    2,
                                                )}{item.data.details.currency}
                                            </td>
                                            <td
                                                class={`px-4 py-3 text-right font-mono ${item.data.details.change >= 0 ? "text-emerald-400" : "text-rose-400"}`}
                                            >
                                                {item.data.details.change > 0
                                                    ? "+"
                                                    : ""}{item.data.details.change_percent?.toFixed(
                                                    2,
                                                )}%
                                            </td>
                                            <td
                                                class="px-4 py-3 text-right text-slate-300"
                                            >
                                                {item.data.kpi?.marketCap
                                                    ? (
                                                          item.data.kpi
                                                              .marketCap / 1e9
                                                      ).toFixed(1) + "B"
                                                    : "-"}
                                            </td>
                                            <td
                                                class="px-4 py-3 text-right text-slate-300"
                                            >
                                                {item.data.kpi?.trailingPE?.toFixed(
                                                    1,
                                                ) || "-"}
                                            </td>
                                            <td
                                                class="px-4 py-3 text-right text-emerald-400"
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
                                                class="px-4 py-3 text-right text-slate-300"
                                            >
                                                {item.data.kpi?.beta?.toFixed(
                                                    2,
                                                ) || "-"}
                                            </td>
                                            <td
                                                class="px-4 py-3 text-right text-blue-400"
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
                                                    class="text-slate-500 hover:text-red-400 p-1"
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
                        class="h-[400px] flex flex-col items-center justify-center text-slate-500 border-2 border-dashed border-white/5 rounded-xl bg-slate-800/10"
                    >
                        <TrendingUp class="w-12 h-12 mb-4 opacity-20" />
                        <p class="text-lg font-medium">No stocks selected</p>
                        <p class="text-sm">
                            Select an index and add companies to compare
                        </p>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>
