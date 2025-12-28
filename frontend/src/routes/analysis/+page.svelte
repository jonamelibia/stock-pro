<script lang="ts">
    import { api, type StockDetails } from "$lib/services/api";
    import StockChart from "$lib/components/StockChart.svelte";
    import {
        Search,
        TrendingUp,
        BarChart2,
        Calendar,
        RefreshCw,
        Activity,
        Plus,
        X,
        Info,
    } from "lucide-svelte";

    // Hardcoded for now, or could fetch from /api/indices
    const INDICES = [
        { symbol: "^IBEX", name: "IBEX 35" },
        { symbol: "^GDAXI", name: "DAX 40" },
        { symbol: "^FCHI", name: "CAC 40" },
        { symbol: "^FTSE", name: "FTSE 100" },
        { symbol: "^STOXX50E", name: "EURO STOXX 50" },
    ];

    let selectedIndex = $state("");
    let constituents: any[] = $state([]);
    let loadingConstituents = $state(false);

    let selectedTicker = $state("");
    let period = $state("1mo"); // Changed default from "6mo" to "1mo"
    let stockData: StockDetails | null = $state(null);
    let loadingStock = $state(false);
    let prediction: any = $state(null); // New state for prediction
    let loadingPrediction = $state(false);
    let error = $state("");

    // Search State
    let indexSearchQuery = $state("");
    let showIndexDropdown = $state(false);

    // Comparison State
    let comparisonSearch = $state("");
    let comparisonList: {
        ticker: string;
        data: StockDetails;
        color: string;
    }[] = $state([]); // Array of { ticker, data, color }
    let showComparisonInput = $state(false);

    const COLORS = [
        "#000000", // Black
        "#D71921", // Retro Accent (Red)
        "#555555", // Grey
        "#aaaaaa", // Light Grey
        "#333333", // Dark Grey
        "#000000", // Black
    ];

    let filteredIndices = $derived(
        INDICES.filter(
            (i) =>
                i.name.toLowerCase().includes(indexSearchQuery.toLowerCase()) ||
                i.symbol.toLowerCase().includes(indexSearchQuery.toLowerCase()),
        ),
    );

    async function loadConstituents() {
        if (!selectedIndex) return;
        loadingConstituents = true;
        constituents = [];
        try {
            constituents = await api.getIndexConstituents(selectedIndex);
        } catch (e) {
            console.error(e);
        } finally {
            loadingConstituents = false;
        }
    }

    async function analyzeStock(ticker: string) {
        if (!ticker) return;
        selectedTicker = ticker;
        loadingStock = true;
        prediction = null; // Clear prediction
        error = "";
        stockData = null; // Clear stockData

        try {
            // 1. Fetch History and Technicals (Fast)
            stockData = await api.getStockDetails(ticker, period);
            if (!stockData || !stockData.history) {
                error = "No data found for this ticker.";
                loadingStock = false;
                return;
            }
            loadingStock = false; // Render fast data

            // If we have comparison items, re-fetch them to match period/normalization
            if (comparisonList.length > 0) {
                await refreshComparisonData();
            } else {
                // 2. Fetch Prediction (Async) if not in comparison mode
                await predictStock(ticker);
            }
        } catch (err) {
            error = "Error fetching stock data.";
            console.error(err);
            loadingStock = false;
        }
    }

    async function addToComparison(ticker: string) {
        if (
            !ticker ||
            comparisonList.find((c) => c.ticker === ticker) ||
            ticker === selectedTicker
        )
            return;

        try {
            loadingStock = true; // Use loadingStock for comparison fetch too
            const data = await api.getStockDetails(ticker, period);

            comparisonList = [
                ...comparisonList,
                {
                    ticker,
                    data,
                    color: COLORS[(comparisonList.length + 1) % COLORS.length],
                },
            ];
            comparisonSearch = "";
            showComparisonInput = false;
        } catch (e) {
            console.error("Error adding comparison:", e);
            error = "Error adding stock to comparison.";
        } finally {
            loadingStock = false;
        }
    }

    function removeComparison(ticker: string) {
        comparisonList = comparisonList.filter((c) => c.ticker !== ticker);
    }

    async function refreshComparisonData() {
        // Refetch all in comparison list with new period
        const promises = comparisonList.map(async (item) => {
            const data = await api.getStockDetails(item.ticker, period);
            return { ...item, data };
        });
        comparisonList = await Promise.all(promises);
    }

    async function predictStock(ticker: string) {
        loadingPrediction = true;
        try {
            const resp = await api.getStockPrediction(ticker, period);
            prediction = resp;
        } catch (e) {
            console.error("Prediction fetch error", e);
            // Non-critical error, charts can still be shown
        } finally {
            loadingPrediction = false;
        }
    }

    // Effect for index change only
    $effect(() => {
        if (selectedIndex) {
            loadConstituents();
            // Clear current analysis when index changes
            stockData = null;
            selectedTicker = "";
            prediction = null; // Clear prediction
            comparisonList = []; // Clear comparison list
        }
    });

    // Chart Data Helpers with Retro Colors
    function getPriceChartData(
        details: StockDetails | null,
        isPredicting: boolean,
    ) {
        if (comparisonList.length > 0) {
            return getComparisonChartData();
        }

        if (!details || !details.history) return { labels: [], datasets: [] };

        const labels = details.history.map((d) =>
            new Date(d.Date).toLocaleDateString(),
        );
        const prices = details.history.map((d) => d.Close);
        const ma50 = details.history.map((d) => d.MA50);
        const bbUpper = details.history.map((d) => d.BB_Upper);
        const bbLower = details.history.map((d) => d.BB_Lower);

        let predictionData: (number | null)[] = [];
        let predictionLabels: string[] = [];

        if (prediction?.forecast) {
            const lastDate = new Date(
                details.history[details.history.length - 1].Date,
            );
            prediction.forecast.forEach((p: number, i: number) => {
                const d = new Date(lastDate);
                d.setDate(d.getDate() + i + 1);
                predictionLabels.push(d.toLocaleDateString());
                predictionData.push(p);
            });

            // To connect the lines, we need the last real price point
            const padding = new Array(prices.length).fill(null);
            padding[padding.length - 1] = prices[prices.length - 1];

            // Final prediction dataset: [null, ..., null, lastPrice, pred1, pred2...]
            predictionData = [...padding, ...predictionData];

            // Extend labels
            labels.push(...predictionLabels);
        }

        return {
            labels,
            datasets: [
                {
                    label: "Close Price",
                    data: prices,
                    borderColor: "#111111",
                    backgroundColor: "transparent",
                    borderWidth: 2,
                    tension: 0,
                    pointRadius: 0,
                    pointHoverRadius: 4,
                },
                {
                    label: "MA50",
                    data: ma50,
                    borderColor: "#555555",
                    borderDash: [5, 5],
                    tension: 0,
                    pointRadius: 0,
                    borderWidth: 1,
                },
                {
                    label: "Bollinger Upper",
                    data: bbUpper,
                    borderColor: "#aaaaaa",
                    backgroundColor: "transparent",
                    tension: 0,
                    pointRadius: 0,
                    borderWidth: 1,
                },
                {
                    label: "Bollinger Lower",
                    data: bbLower,
                    borderColor: "#aaaaaa",
                    backgroundColor: "transparent",
                    tension: 0,
                    pointRadius: 0,
                    borderWidth: 1,
                },
                ...(prediction
                    ? [
                          {
                              label: "AI Forecast",
                              data: predictionData,
                              borderColor: "#D71921",
                              borderWidth: 2,
                              borderDash: [2, 2],
                              tension: 0,
                              pointRadius: 0,
                          },
                      ]
                    : []),
            ],
        };
    }

    function getComparisonChartData() {
        if (!stockData || !stockData.history)
            return { labels: [], datasets: [] };

        // Simple normalization: Compare % change from start of period
        const labels = stockData.history.map((d) =>
            new Date(d.Date).toLocaleDateString(),
        );

        const datasets = [
            {
                label: selectedTicker,
                data: stockData.history.map((d, i) => {
                    const startPrice = stockData.history[0].Close;
                    return ((d.Close - startPrice) / startPrice) * 100;
                }),
                borderColor: COLORS[0],
                backgroundColor: "transparent",
                borderWidth: 2,
                tension: 0,
                pointRadius: 0,
            },
        ];

        comparisonList.forEach((item) => {
            if (item.data && item.data.history) {
                datasets.push({
                    label: item.ticker,
                    data: item.data.history.map((d, i) => {
                        const startPrice = item.data.history[0].Close;
                        return ((d.Close - startPrice) / startPrice) * 100;
                    }),
                    borderColor: item.color,
                    backgroundColor: "transparent",
                    borderWidth: 2,
                    tension: 0,
                    pointRadius: 0,
                });
            }
        });

        return { labels, datasets };
    }

    function getIndicatorChartData(details: StockDetails) {
        if (!details || !details.history) return { labels: [], datasets: [] };
        const labels = details.history.map((d) => d.Date);
        const rsi = details.history.map((d) => d.RSI);

        return {
            labels,
            datasets: [
                {
                    label: "RSI (14)",
                    data: rsi,
                    borderColor: "#111111",
                    backgroundColor: "rgba(0,0,0, 0.05)",
                    borderWidth: 2,
                    tension: 0,
                    pointRadius: 0,
                    fill: true,
                },
            ],
        };
    }
</script>

<div
    class="h-[calc(100vh-6rem)] flex flex-col md:flex-row gap-6 p-4 bg-retro-surface font-mono text-retro-fg"
>
    <!-- Sidebar / Selection Area -->
    <div
        class="w-full md:w-1/3 flex flex-col gap-4 bg-white border border-retro p-6 overflow-hidden"
    >
        <div class="flex items-center gap-3 mb-2 border-b border-retro pb-4">
            <div class="p-2 border border-retro bg-retro-accent text-white">
                <BarChart2 class="w-6 h-6" />
            </div>
            <h2
                class="text-xl font-display uppercase tracking-widest text-retro-fg"
            >
                Scanner
            </h2>
        </div>

        <!-- Index Selection -->
        <div class="space-y-2">
            <label
                for="index-select"
                class="text-xs font-bold uppercase tracking-wider pl-1"
                >Market Index</label
            >
            <div class="relative">
                <select
                    id="index-select"
                    bind:value={selectedIndex}
                    class="w-full bg-white border border-retro text-sm focus:ring-0 focus:border-retro-accent p-3 appearance-none cursor-pointer hover:bg-retro-surface transition-colors rounded-none"
                >
                    <option value="">SELECT INDEX</option>
                    {#each INDICES as idx}
                        <option value={idx.symbol}>{idx.name}</option>
                    {/each}
                </select>
                <div
                    class="absolute right-3 top-3.5 pointer-events-none text-retro-fg"
                >
                    <TrendingUp class="w-4 h-4" />
                </div>
            </div>
        </div>

        <!-- Constituents List -->
        <div
            class="flex-grow flex flex-col min-h-0 bg-white border border-retro p-2"
        >
            {#if loadingConstituents}
                <div
                    class="flex flex-col items-center justify-center h-full gap-3"
                >
                    <div
                        class="animate-spin h-8 w-8 border-4 border-retro border-t-retro-accent rounded-full"
                    ></div>
                    <span class="text-xs uppercase animate-pulse"
                        >Loading...</span
                    >
                </div>
            {:else if constituents.length > 0}
                <div class="overflow-y-auto pr-2 custom-scrollbar space-y-1">
                    {#each constituents as company}
                        <button
                            onclick={() => analyzeStock(company.ticker)}
                            class={`w-full group text-left px-3 py-3 transition-none border border-transparent flex justify-between items-center ${
                                selectedTicker === company.ticker
                                    ? "bg-retro-accent text-white border-retro"
                                    : "hover:bg-retro-surface hover:border-retro text-retro-fg"
                            }`}
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class={`w-8 h-8 border border-retro flex items-center justify-center text-xs font-bold ${selectedTicker === company.ticker ? "bg-white text-retro-accent" : "bg-retro-surface text-retro-fg"}`}
                                >
                                    {company.ticker.substring(0, 2)}
                                </div>
                                <div class="flex flex-col">
                                    <span class="font-bold text-sm font-mono"
                                        >{company.ticker}</span
                                    >
                                    <span
                                        class={`text-[10px] uppercase tracking-wider truncate max-w-[120px] ${selectedTicker === company.ticker ? "text-white" : "text-gray-500"}`}
                                        >{company.name}</span
                                    >
                                </div>
                            </div>

                            {#if company.change_percent !== undefined}
                                <span
                                    class={`text-xs font-mono font-bold px-2 py-1 border border-retro ${company.change_percent >= 0 ? "bg-white text-retro-fg" : "bg-retro-fg text-white"}`}
                                >
                                    {company.change_percent > 0
                                        ? "+"
                                        : ""}{company.change_percent}%
                                </span>
                            {/if}
                        </button>
                    {/each}
                </div>
            {:else if selectedIndex}
                <div
                    class="flex flex-col items-center justify-center h-full text-gray-500 p-4 text-center"
                >
                    <Search class="w-8 h-8 mb-2 opacity-50" />
                    <p class="text-sm uppercase">No constituents found.</p>
                </div>
            {:else}
                <div
                    class="flex flex-col items-center justify-center h-full text-gray-500 p-4 text-center"
                >
                    <TrendingUp class="w-8 h-8 mb-2 opacity-50" />
                    <p class="text-sm uppercase">Select an index</p>
                </div>
            {/if}
        </div>
    </div>

    <!-- Main Analysis Area -->
    <div class="w-full md:w-2/3 flex flex-col gap-6 overflow-hidden">
        {#if stockData}
            <div
                class="h-full flex flex-col gap-6 overflow-y-auto pr-2 custom-scrollbar"
            >
                <!-- Header Card -->
                <div class="bg-white border border-retro p-6">
                    <div
                        class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-retro pb-4"
                    >
                        <div>
                            <div class="flex items-center gap-2">
                                <h2
                                    class="text-3xl font-display uppercase tracking-tighter text-retro-fg"
                                >
                                    {selectedTicker}
                                </h2>
                                <span
                                    class="flex items-center gap-1 px-2 py-0.5 border border-retro bg-retro-surface text-xs font-bold uppercase"
                                >
                                    {#if loadingPrediction}
                                        <div
                                            class="w-2 h-2 border-t border-r border-retro-accent animate-spin"
                                        ></div>
                                        Predicting...
                                    {:else}
                                        AI Enabled
                                    {/if}
                                </span>
                                <!-- Comparison Controls -->
                                <div class="relative ml-4">
                                    {#if !showComparisonInput}
                                        <button
                                            class="flex items-center gap-1 text-xs uppercase font-bold hover:bg-retro-surface px-3 py-1.5 transition-colors border border-retro"
                                            onclick={() =>
                                                (showComparisonInput = true)}
                                        >
                                            <Plus class="w-3 h-3" />
                                            Compare
                                        </button>
                                    {:else}
                                        <div
                                            class="flex items-center absolute left-0 md:relative z-10 top-0 bg-white border border-retro p-1"
                                        >
                                            <input
                                                type="text"
                                                class="bg-white border-b border-retro px-2 py-1 text-xs text-retro-fg focus:outline-none w-32 font-mono uppercase"
                                                placeholder="Ticker..."
                                                bind:value={comparisonSearch}
                                                onkeydown={(e) =>
                                                    e.key === "Enter" &&
                                                    addToComparison(
                                                        comparisonSearch.toUpperCase(),
                                                    )}
                                                autofocus
                                            />
                                            <button
                                                class="bg-retro-accent text-white px-2 py-1 text-xs font-bold uppercase hover:bg-black transition-colors ml-2"
                                                onclick={() =>
                                                    addToComparison(
                                                        comparisonSearch.toUpperCase(),
                                                    )}
                                            >
                                                Add
                                            </button>
                                            <button
                                                class="ml-2 text-retro-fg hover:text-retro-accent"
                                                onclick={() =>
                                                    (showComparisonInput = false)}
                                            >
                                                <X class="w-4 h-4" />
                                            </button>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                            <p
                                class="text-sm text-gray-500 mt-1 font-mono uppercase"
                            >
                                Technical Analysis • Chronos Forecast
                            </p>
                        </div>

                        <div
                            class="flex items-center gap-2 border border-retro p-1"
                        >
                            <Calendar class="w-4 h-4 text-retro-fg ml-2" />
                            <select
                                bind:value={period}
                                onchange={() => analyzeStock(selectedTicker)}
                                class="bg-transparent border-none text-sm text-retro-fg focus:ring-0 cursor-pointer py-1 pr-8 pl-1 font-mono uppercase"
                            >
                                <option value="1mo">1 Month</option>
                                <option value="3mo">3 Months</option>
                                <option value="6mo">6 Months</option>
                                <option value="1y">1 Year</option>
                            </select>
                        </div>
                    </div>

                    <!-- Comparison Tags -->
                    {#if comparisonList.length > 0}
                        <div class="flex flex-wrap gap-2 pt-4">
                            <div
                                class="flex items-center gap-1.5 px-3 py-1 border border-retro bg-white"
                            >
                                <span
                                    class="w-3 h-3 border border-black"
                                    style="background-color: {COLORS[0]}"
                                ></span>
                                <span class="text-xs font-bold uppercase"
                                    >{selectedTicker}</span
                                >
                            </div>
                            {#each comparisonList as item}
                                <div
                                    class="flex items-center gap-1.5 px-3 py-1 border border-retro bg-white"
                                >
                                    <span
                                        class="w-3 h-3 border border-black"
                                        style="background-color: {item.color}"
                                    ></span>
                                    <span class="text-xs font-bold uppercase"
                                        >{item.ticker}</span
                                    >
                                    <button
                                        class="ml-1 text-gray-500 hover:text-retro-accent"
                                        onclick={() =>
                                            removeComparison(item.ticker)}
                                    >
                                        <X class="w-3 h-3" />
                                    </button>
                                </div>
                            {/each}
                        </div>
                    {/if}
                </div>

                <!-- Stock Description -->
                {#if stockData.kpi.description && comparisonList.length === 0}
                    <div class="bg-white border border-retro p-4">
                        <h3
                            class="text-xs font-bold uppercase tracking-wider mb-2 flex items-center gap-2 border-b border-retro pb-2"
                        >
                            <Info class="w-3 h-3" /> About {selectedTicker}
                        </h3>
                        <p
                            class="text-sm text-retro-fg leading-relaxed font-mono"
                        >
                            {stockData.kpi.description}
                        </p>
                    </div>
                {/if}

                {#if comparisonList.length > 0}
                    <!-- Comparison Table -->
                    <div
                        class="bg-white border border-retro p-4 mb-6 overflow-x-auto"
                    >
                        <table class="w-full text-left text-sm font-mono">
                            <thead
                                class="text-xs uppercase border-b border-retro"
                            >
                                <tr>
                                    <th class="py-2 px-3">Ticker</th>
                                    <th class="py-2 px-3 text-right">Price</th>
                                    <th class="py-2 px-3 text-right">Mkt Cap</th
                                    >
                                    <th class="py-2 px-3 text-right">P/E</th>
                                    <th class="py-2 px-3 text-right">Yield</th>
                                    <th class="py-2 px-3 text-right">Beta</th>
                                    <th class="py-2 px-3 text-right">ROE</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-retro">
                                <tr class="hover:bg-retro-surface">
                                    <td
                                        class="py-2 px-3 font-bold flex items-center gap-2"
                                    >
                                        <span
                                            class="w-2 h-2 border border-black"
                                            style="background-color: {COLORS[0]}"
                                        ></span>
                                        {selectedTicker}
                                    </td>
                                    <td class="py-2 px-3 text-right"
                                        >{stockData.details.price?.toFixed(
                                            2,
                                        )}{stockData.details.currency}</td
                                    >
                                    <td
                                        class="py-2 px-3 text-right text-gray-600"
                                        >{stockData.kpi.marketCap
                                            ? (
                                                  stockData.kpi.marketCap / 1e9
                                              ).toFixed(1) + "B"
                                            : "-"}</td
                                    >
                                    <td
                                        class="py-2 px-3 text-right text-gray-600"
                                        >{stockData.kpi.trailingPE?.toFixed(
                                            1,
                                        ) || "-"}</td
                                    >
                                    <td
                                        class="py-2 px-3 text-right text-retro-accent"
                                        >{stockData.kpi.dividendYield
                                            ? (
                                                  stockData.kpi.dividendYield *
                                                  100
                                              ).toFixed(2) + "%"
                                            : "-"}</td
                                    >
                                    <td
                                        class="py-2 px-3 text-right text-gray-600"
                                        >{stockData.kpi.beta?.toFixed(2) ||
                                            "-"}</td
                                    >
                                    <td
                                        class="py-2 px-3 text-right text-blue-600"
                                        >{stockData.kpi.returnOnEquity
                                            ? (
                                                  stockData.kpi.returnOnEquity *
                                                  100
                                              ).toFixed(1) + "%"
                                            : "-"}</td
                                    >
                                </tr>
                                {#each comparisonList as item}
                                    {@const itemData = item.data}
                                    <tr class="hover:bg-retro-surface">
                                        <td
                                            class="py-2 px-3 font-bold flex items-center gap-2"
                                        >
                                            <span
                                                class="w-2 h-2 border border-black"
                                                style="background-color: {item.color}"
                                            ></span>
                                            {item.ticker}
                                        </td>
                                        <td class="py-2 px-3 text-right"
                                            >{itemData.details?.price?.toFixed(
                                                2,
                                            )}{itemData.details?.currency}</td
                                        >
                                        <td
                                            class="py-2 px-3 text-right text-gray-600"
                                            >{itemData.kpi?.marketCap
                                                ? (
                                                      itemData.kpi.marketCap /
                                                      1e9
                                                  ).toFixed(1) + "B"
                                                : "-"}</td
                                        >
                                        <td
                                            class="py-2 px-3 text-right text-gray-600"
                                            >{itemData.kpi?.trailingPE?.toFixed(
                                                1,
                                            ) || "-"}</td
                                        >
                                        <td
                                            class="py-2 px-3 text-right text-retro-accent"
                                            >{itemData.kpi?.dividendYield
                                                ? (
                                                      itemData.kpi
                                                          .dividendYield * 100
                                                  ).toFixed(2) + "%"
                                                : "-"}</td
                                        >
                                        <td
                                            class="py-2 px-3 text-right text-gray-600"
                                            >{itemData.kpi?.beta?.toFixed(2) ||
                                                "-"}</td
                                        >
                                        <td
                                            class="py-2 px-3 text-right text-blue-600"
                                            >{itemData.kpi?.returnOnEquity
                                                ? (
                                                      itemData.kpi
                                                          .returnOnEquity * 100
                                                  ).toFixed(1) + "%"
                                                : "-"}</td
                                        >
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                {:else}
                    <!-- Single Stock Details Grid -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <!-- Fundamentals Card -->
                        <div class="bg-white border border-retro p-6">
                            <div
                                class="flex items-center gap-2 mb-4 border-b border-retro pb-2"
                            >
                                <Activity class="w-4 h-4 text-retro-accent" />
                                <h3
                                    class="text-lg font-bold font-display uppercase"
                                >
                                    Fundamentals
                                </h3>
                            </div>
                            <div class="grid grid-cols-2 gap-4">
                                <div
                                    class="bg-retro-surface p-3 border border-retro"
                                >
                                    <p
                                        class="text-[10px] text-gray-500 uppercase font-bold mb-1"
                                    >
                                        Price
                                    </p>
                                    <p class="text-xl font-bold font-display">
                                        {stockData.details.price?.toFixed(
                                            2,
                                        )}{stockData.details.currency}
                                    </p>
                                </div>
                                <div
                                    class="bg-retro-surface p-3 border border-retro"
                                >
                                    <p
                                        class="text-[10px] text-gray-500 uppercase font-bold mb-1"
                                    >
                                        Change
                                    </p>
                                    <p
                                        class={`text-xl font-bold font-display ${stockData.details.change >= 0 ? "text-retro-fg" : "text-retro-accent"}`}
                                    >
                                        {stockData.details.change > 0
                                            ? "+"
                                            : ""}{stockData.details.change}
                                        <span class="text-xs"
                                            >({stockData.details
                                                .change_percent}%)</span
                                        >
                                    </p>
                                </div>
                                <div
                                    class="bg-retro-surface p-3 border border-retro"
                                >
                                    <p
                                        class="text-[10px] text-gray-500 uppercase font-bold mb-1"
                                    >
                                        P/E Ratio
                                    </p>
                                    <p class="text-lg font-bold font-mono">
                                        {stockData.kpi.trailingPE?.toFixed(2) ||
                                            "N/A"}
                                    </p>
                                </div>
                                <div
                                    class="bg-retro-surface p-3 border border-retro"
                                >
                                    <p
                                        class="text-[10px] text-gray-500 uppercase font-bold mb-1"
                                    >
                                        Market Cap
                                    </p>
                                    <p class="text-lg font-bold font-mono">
                                        {stockData.kpi.marketCap
                                            ? (
                                                  stockData.kpi.marketCap / 1e9
                                              ).toFixed(1) + "B"
                                            : "N/A"}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Technicals Card -->
                        <div class="bg-white border border-retro p-6">
                            <div
                                class="flex items-center gap-2 mb-4 border-b border-retro pb-2"
                            >
                                <TrendingUp class="w-4 h-4 text-retro-accent" />
                                <h3
                                    class="text-lg font-bold font-display uppercase"
                                >
                                    Technicals
                                </h3>
                            </div>
                            <div class="grid grid-cols-2 gap-4">
                                <div
                                    class="bg-retro-surface p-3 border border-retro"
                                >
                                    <p
                                        class="text-[10px] text-gray-500 uppercase font-bold mb-1"
                                    >
                                        RSI (14)
                                    </p>
                                    <div class="flex items-end gap-2">
                                        <p
                                            class="text-xl font-bold font-display"
                                        >
                                            {stockData.details.history[
                                                stockData.details.history
                                                    .length - 1
                                            ]?.RSI?.toFixed(0) || "-"}
                                        </p>
                                        <span
                                            class="text-xs mb-1 {stockData
                                                .details.history[
                                                stockData.details.history
                                                    .length - 1
                                            ]?.RSI > 70
                                                ? 'text-retro-accent'
                                                : 'text-gray-500'}"
                                        >
                                            {stockData.details.history[
                                                stockData.details.history
                                                    .length - 1
                                            ]?.RSI > 70
                                                ? "OVERBOUGHT"
                                                : stockData.details.history[
                                                        stockData.details
                                                            .history.length - 1
                                                    ]?.RSI < 30
                                                  ? "OVERSOLD"
                                                  : "NEUTRAL"}
                                        </span>
                                    </div>
                                </div>
                                <div
                                    class="bg-retro-surface p-3 border border-retro"
                                >
                                    <p
                                        class="text-[10px] text-gray-500 uppercase font-bold mb-1"
                                    >
                                        MACD
                                    </p>
                                    <p class="text-xl font-bold font-display">
                                        {stockData.details.history[
                                            stockData.details.history.length - 1
                                        ]?.MACD?.toFixed(2) || "-"}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                {/if}

                <!-- Charts -->
                <div class="grid grid-cols-1 gap-6">
                    <!-- Price Chart -->
                    <div class="bg-white border border-retro p-4 h-[400px]">
                        <h3
                            class="text-sm font-bold uppercase mb-4 font-display border-b border-retro inline-block"
                        >
                            Price History & Forecast
                        </h3>
                        <StockChart
                            data={getPriceChartData(
                                stockData.details,
                                loadingPrediction,
                            )}
                            title=""
                        />
                    </div>

                    <!-- RSI Chart -->
                    {#if comparisonList.length === 0}
                        <div class="bg-white border border-retro p-4 h-[300px]">
                            <h3
                                class="text-sm font-bold uppercase mb-4 font-display border-b border-retro inline-block"
                            >
                                RSI Indicator
                            </h3>
                            <StockChart
                                data={getIndicatorChartData(stockData.details)}
                                title=""
                            />
                        </div>
                    {/if}
                </div>
            </div>
        {:else if loadingStock}
            <div
                class="h-full flex flex-col items-center justify-center gap-4 bg-white border border-retro"
            >
                <div
                    class="animate-spin h-12 w-12 border-4 border-retro border-t-retro-accent rounded-full"
                ></div>
                <p class="text-lg font-mono uppercase animate-pulse">
                    Analyzing Market Data...
                </p>
            </div>
        {:else}
            <div
                class="h-full flex flex-col items-center justify-center gap-4 bg-white border border-retro"
            >
                <div
                    class="bg-retro-surface p-8 rounded-full border border-retro"
                >
                    <TrendingUp class="w-16 h-16 text-retro-fg opacity-50" />
                </div>
                <h3 class="text-xl font-display uppercase tracking-widest">
                    Ready to Analyze
                </h3>
                <p class="text-sm text-gray-500 font-mono uppercase">
                    Select a stock from the sidebar to begin
                </p>
            </div>
        {/if}
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

    .fade-in {
        animation: fadeIn 0.4s steps(4) forwards; /* Retro steps animation */
        opacity: 0;
    }

    @keyframes fadeIn {
        to {
            opacity: 1;
        }
    }
</style>
