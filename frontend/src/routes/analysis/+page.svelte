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
        "#3b82f6", // Blue (Main)
        "#ef4444", // Red
        "#10b981", // Emerald
        "#f59e0b", // Amber
        "#8b5cf6", // Violet
        "#ec4899", // Pink
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

    // Chart Data Helpers with Neon Colors
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
                    borderColor: "#3b82f6",
                    backgroundColor: "rgba(59, 130, 246, 0.1)",
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 0,
                    pointHoverRadius: 4,
                },
                {
                    label: "MA50",
                    data: ma50,
                    borderColor: "#f59e0b",
                    borderDash: [5, 5],
                    tension: 0.3,
                    pointRadius: 0,
                    borderWidth: 1,
                },
                {
                    label: "Bollinger Upper",
                    data: bbUpper,
                    borderColor: "rgba(255, 255, 255, 0.1)",
                    backgroundColor: "rgba(255, 255, 255, 0.02)",
                    tension: 0.3,
                    pointRadius: 0,
                    borderWidth: 1,
                    fill: "+1",
                },
                {
                    label: "Bollinger Lower",
                    data: bbLower,
                    borderColor: "rgba(255, 255, 255, 0.1)",
                    backgroundColor: "rgba(255, 255, 255, 0.02)",
                    tension: 0.3,
                    pointRadius: 0,
                    borderWidth: 1,
                    fill: false,
                },
                ...(prediction
                    ? [
                          {
                              label: "AI Forecast",
                              data: predictionData,
                              borderColor: "#10b981",
                              borderWidth: 2,
                              borderDash: [5, 5],
                              tension: 0.4,
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
                tension: 0.3,
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
                    tension: 0.3,
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
                    borderColor: "#8b5cf6", // Violet-500
                    backgroundColor: "rgba(139, 92, 246, 0.1)",
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 0,
                    fill: true,
                },
            ],
        };
    }
</script>

<div class="h-[calc(100vh-6rem)] flex flex-col md:flex-row gap-6 p-1">
    <!-- Sidebar / Selection Area -->
    <div
        class="w-full md:w-1/3 flex flex-col gap-4 bg-slate-800/30 backdrop-blur-xl border border-white/5 shadow-2xl rounded-2xl p-6 overflow-hidden"
    >
        <div class="flex items-center gap-3 mb-2">
            <div class="p-2 rounded-lg bg-blue-500/20 text-blue-400">
                <BarChart2 class="w-6 h-6" />
            </div>
            <h2
                class="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
            >
                Market Scanner
            </h2>
        </div>

        <!-- Index Selection -->
        <div class="space-y-2">
            <label
                for="index-select"
                class="text-xs font-semibold text-slate-400 uppercase tracking-wider pl-1"
                >Market Index</label
            >
            <div class="relative">
                <select
                    id="index-select"
                    bind:value={selectedIndex}
                    class="w-full bg-slate-900/50 border border-white/10 text-white text-sm rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent p-3 appearance-none cursor-pointer hover:bg-slate-900/70 transition-colors"
                >
                    <option value="">Select a European Index</option>
                    {#each INDICES as idx}
                        <option value={idx.symbol}>{idx.name}</option>
                    {/each}
                </select>
                <div
                    class="absolute right-3 top-3.5 pointer-events-none text-slate-500"
                >
                    <TrendingUp class="w-4 h-4" />
                </div>
            </div>
        </div>

        <!-- Constituents List -->
        <div
            class="flex-grow flex flex-col min-h-0 bg-slate-900/30 rounded-xl border border-white/5 p-2"
        >
            {#if loadingConstituents}
                <div
                    class="flex flex-col items-center justify-center h-full gap-3"
                >
                    <div
                        class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"
                    ></div>
                    <span class="text-xs text-slate-500 animate-pulse"
                        >Loading Constituents...</span
                    >
                </div>
            {:else if constituents.length > 0}
                <div class="overflow-y-auto pr-2 custom-scrollbar space-y-1">
                    {#each constituents as company}
                        <button
                            onclick={() => analyzeStock(company.ticker)}
                            class={`w-full group text-left px-3 py-3 rounded-lg transition-all border border-transparent flex justify-between items-center ${
                                selectedTicker === company.ticker
                                    ? "bg-blue-600/20 border-blue-500/50 shadow-[0_0_15px_rgba(37,99,235,0.2)]"
                                    : "hover:bg-white/5 hover:border-white/10"
                            }`}
                        >
                            <div class="flex items-center gap-3">
                                <div
                                    class={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${selectedTicker === company.ticker ? "bg-blue-500 text-white" : "bg-slate-700 text-slate-300"}`}
                                >
                                    {company.ticker.substring(0, 2)}
                                </div>
                                <div class="flex flex-col">
                                    <span
                                        class={`font-medium text-sm ${selectedTicker === company.ticker ? "text-white" : "text-slate-300 group-hover:text-white"}`}
                                        >{company.ticker}</span
                                    >
                                    <span
                                        class="text-[10px] text-slate-500 uppercase tracking-wider truncate max-w-[120px]"
                                        >{company.name}</span
                                    >
                                </div>
                            </div>

                            {#if company.change_percent !== undefined}
                                <span
                                    class={`text-xs font-mono font-medium px-2 py-1 rounded ${
                                        company.change_percent >= 0
                                            ? "bg-emerald-500/10 text-emerald-400"
                                            : "bg-rose-500/10 text-rose-400"
                                    }`}
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
                    class="flex flex-col items-center justify-center h-full text-slate-500 p-4 text-center"
                >
                    <Search class="w-8 h-8 mb-2 opacity-50" />
                    <p class="text-sm">No constituents found.</p>
                </div>
            {:else}
                <div
                    class="flex flex-col items-center justify-center h-full text-slate-500 p-4 text-center"
                >
                    <TrendingUp class="w-8 h-8 mb-2 opacity-50" />
                    <p class="text-sm">Select an index to view companies</p>
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
                <div
                    class="bg-slate-800/30 backdrop-blur-xl border border-white/5 shadow-2xl rounded-2xl p-6 fade-in"
                >
                    <div
                        class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6"
                    >
                        <div>
                            <div class="flex items-center gap-2">
                                <h2
                                    class="text-3xl font-bold text-white tracking-tight"
                                >
                                    {selectedTicker}
                                </h2>
                                <span
                                    class="flex items-center gap-1 px-2 py-0.5 rounded-full bg-blue-500/20 border border-blue-500/30 text-blue-400 text-xs font-bold uppercase"
                                >
                                    {#if loadingPrediction}
                                        <div
                                            class="w-2 h-2 rounded-full border-t border-r border-blue-400 animate-spin"
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
                                            class="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 bg-blue-500/10 hover:bg-blue-500/20 px-3 py-1.5 rounded-full transition-colors border border-blue-500/20"
                                            onclick={() =>
                                                (showComparisonInput = true)}
                                        >
                                            <Plus class="w-3 h-3" />
                                            Compare
                                        </button>
                                    {:else}
                                        <div
                                            class="flex items-center animate-in fade-in slide-in-from-left-2 duration-200 absolute left-0 md:relative z-10 top-0"
                                        >
                                            <input
                                                type="text"
                                                class="bg-slate-900 border border-blue-500/30 rounded-l-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500 w-32"
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
                                                class="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded-r-lg text-xs font-medium transition-colors"
                                                onclick={() =>
                                                    addToComparison(
                                                        comparisonSearch.toUpperCase(),
                                                    )}
                                            >
                                                Add
                                            </button>
                                            <button
                                                class="ml-2 text-slate-500 hover:text-white"
                                                onclick={() =>
                                                    (showComparisonInput = false)}
                                            >
                                                <X class="w-4 h-4" />
                                            </button>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                            <p class="text-sm text-slate-400 mt-1">
                                Technical Analysis • 30 Day Chronos Forecast
                            </p>
                        </div>

                        <div
                            class="flex items-center gap-2 bg-slate-900/50 p-1 rounded-lg border border-white/10"
                        >
                            <Calendar class="w-4 h-4 text-slate-400 ml-2" />
                            <select
                                bind:value={period}
                                onchange={() => analyzeStock(selectedTicker)}
                                class="bg-transparent border-none text-sm text-white focus:ring-0 cursor-pointer py-1 pr-8 pl-1"
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
                        <div
                            class="flex flex-wrap gap-2 pt-4 border-t border-white/5"
                        >
                            <div
                                class="flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 border border-white/10"
                            >
                                <span
                                    class="w-2 h-2 rounded-full"
                                    style="background-color: {COLORS[0]}"
                                ></span>
                                <span class="text-xs font-bold text-white"
                                    >{selectedTicker}</span
                                >
                            </div>
                            {#each comparisonList as item}
                                <div
                                    class="flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 border border-white/10 animate-in fade-in zoom-in duration-200"
                                >
                                    <span
                                        class="w-2 h-2 rounded-full"
                                        style="background-color: {item.color}"
                                    ></span>
                                    <span class="text-xs font-bold text-white"
                                        >{item.ticker}</span
                                    >
                                    <button
                                        class="ml-1 text-slate-500 hover:text-red-400"
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
                    <div
                        class="bg-slate-800/20 rounded-xl border border-white/5 p-4 fade-in"
                    >
                        <h3
                            class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-2"
                        >
                            <Info class="w-3 h-3" /> About {selectedTicker}
                        </h3>
                        <p class="text-sm text-slate-300 leading-relaxed">
                            {stockData.kpi.description}
                        </p>
                    </div>
                {/if}

                {#if comparisonList.length > 0}
                    <!-- Comparison Table -->
                    <div
                        class="bg-slate-800/30 rounded-xl border border-white/5 p-4 mb-6 overflow-x-auto fade-in"
                    >
                        <table class="w-full text-left text-sm">
                            <thead
                                class="text-xs text-slate-500 uppercase border-b border-white/5"
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
                            <tbody class="divide-y divide-white/5">
                                <tr class="hover:bg-white/5">
                                    <td
                                        class="py-2 px-3 font-bold text-white flex items-center gap-2"
                                    >
                                        <span
                                            class="w-2 h-2 rounded-full"
                                            style="background-color: {COLORS[0]}"
                                        ></span>
                                        {selectedTicker}
                                    </td>
                                    <td class="py-2 px-3 text-right text-white">
                                        {stockData.details.price?.toFixed(
                                            2,
                                        )}{stockData.details.currency}
                                    </td>
                                    <td
                                        class="py-2 px-3 text-right text-slate-300"
                                    >
                                        {stockData.kpi.marketCap
                                            ? (
                                                  stockData.kpi.marketCap / 1e9
                                              ).toFixed(1) + "B"
                                            : "-"}
                                    </td>
                                    <td
                                        class="py-2 px-3 text-right text-slate-300"
                                        >{stockData.kpi.trailingPE?.toFixed(
                                            1,
                                        ) || "-"}</td
                                    >
                                    <td
                                        class="py-2 px-3 text-right text-emerald-400"
                                        >{stockData.kpi.dividendYield
                                            ? (
                                                  stockData.kpi.dividendYield *
                                                  100
                                              ).toFixed(2) + "%"
                                            : "-"}</td
                                    >
                                    <td
                                        class="py-2 px-3 text-right text-slate-300"
                                        >{stockData.kpi.beta?.toFixed(2) ||
                                            "-"}</td
                                    >
                                    <td
                                        class="py-2 px-3 text-right text-blue-400"
                                        >{stockData.kpi.returnOnEquity
                                            ? (
                                                  stockData.kpi.returnOnEquity *
                                                  100
                                              ).toFixed(1) + "%"
                                            : "-"}</td
                                    >
                                </tr>
                                {#each comparisonList as item}
                                    {@const itemData =
                                        item.data as StockDetails}
                                    <tr class="hover:bg-white/5">
                                        <td
                                            class="py-2 px-3 font-bold text-white flex items-center gap-2"
                                        >
                                            <span
                                                class="w-2 h-2 rounded-full"
                                                style="background-color: {item.color}"
                                            ></span>
                                            {item.ticker}
                                        </td>
                                        <td
                                            class="py-2 px-3 text-right text-white"
                                        >
                                            {itemData.details?.price?.toFixed(
                                                2,
                                            )}{itemData.details?.currency}
                                        </td>
                                        <td
                                            class="py-2 px-3 text-right text-slate-300"
                                        >
                                            {itemData.kpi?.marketCap
                                                ? (
                                                      itemData.kpi.marketCap /
                                                      1e9
                                                  ).toFixed(1) + "B"
                                                : "-"}
                                        </td>
                                        <td
                                            class="py-2 px-3 text-right text-slate-300"
                                            >{itemData.kpi?.trailingPE?.toFixed(
                                                1,
                                            ) || "-"}</td
                                        >
                                        <td
                                            class="py-2 px-3 text-right text-emerald-400"
                                            >{itemData.kpi?.dividendYield
                                                ? (
                                                      itemData.kpi
                                                          .dividendYield * 100
                                                  ).toFixed(2) + "%"
                                                : "-"}</td
                                        >
                                        <td
                                            class="py-2 px-3 text-right text-slate-300"
                                            >{itemData.kpi?.beta?.toFixed(2) ||
                                                "-"}</td
                                        >
                                        <td
                                            class="py-2 px-3 text-right text-blue-400"
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
                        <div
                            class="bg-slate-800/30 rounded-2xl border border-white/5 p-6"
                        >
                            <div class="flex items-center gap-2 mb-4">
                                <Activity class="w-4 h-4 text-emerald-400" />
                                <h3 class="text-lg font-bold text-white">
                                    Fundamentals
                                </h3>
                            </div>
                            <div class="grid grid-cols-2 gap-4">
                                <div
                                    class="bg-slate-900/50 p-3 rounded-xl border border-white/5"
                                >
                                    <p
                                        class="text-[10px] text-slate-500 uppercase font-bold mb-1"
                                    >
                                        Price
                                    </p>
                                    <p class="text-xl font-bold text-white">
                                        {stockData.details.price?.toFixed(
                                            2,
                                        )}{stockData.details.currency}
                                    </p>
                                </div>
                                <div
                                    class="bg-slate-900/50 p-3 rounded-xl border border-white/5"
                                >
                                    <p
                                        class="text-[10px] text-slate-500 uppercase font-bold mb-1"
                                    >
                                        Change
                                    </p>
                                    <p
                                        class={`text-xl font-bold ${stockData.details.change >= 0 ? "text-emerald-400" : "text-rose-400"}`}
                                    >
                                        {stockData.details.change > 0
                                            ? "+"
                                            : ""}{stockData.details.change_percent?.toFixed(
                                            2,
                                        )}%
                                    </p>
                                </div>
                                <div
                                    class="bg-slate-900/50 p-3 rounded-xl border border-white/5"
                                >
                                    <p
                                        class="text-[10px] text-slate-500 uppercase font-bold mb-1"
                                    >
                                        Mkt Cap
                                    </p>
                                    <p class="text-sm font-bold text-white">
                                        {stockData.kpi.marketCap
                                            ? (
                                                  stockData.kpi.marketCap / 1e9
                                              ).toFixed(1) + "B"
                                            : "N/A"}
                                    </p>
                                </div>
                                <div
                                    class="bg-slate-900/50 p-3 rounded-xl border border-white/5"
                                >
                                    <p
                                        class="text-[10px] text-slate-500 uppercase font-bold mb-1"
                                    >
                                        P/E Ratio
                                    </p>
                                    <p class="text-sm font-bold text-white">
                                        {stockData.kpi.trailingPE?.toFixed(1) ||
                                            "N/A"}
                                    </p>
                                </div>
                                <div
                                    class="bg-slate-900/50 p-3 rounded-xl border border-white/5"
                                >
                                    <p
                                        class="text-[10px] text-slate-500 uppercase font-bold mb-1"
                                    >
                                        ROE
                                    </p>
                                    <p class="text-sm font-bold text-blue-400">
                                        {stockData.kpi.returnOnEquity
                                            ? (
                                                  stockData.kpi.returnOnEquity *
                                                  100
                                              ).toFixed(1) + "%"
                                            : "N/A"}
                                    </p>
                                </div>
                                <div
                                    class="bg-slate-900/50 p-3 rounded-xl border border-white/5"
                                >
                                    <p
                                        class="text-[10px] text-slate-500 uppercase font-bold mb-1"
                                    >
                                        Margins
                                    </p>
                                    <p
                                        class="text-sm font-bold text-emerald-400"
                                    >
                                        {stockData.kpi.profitMargins
                                            ? (
                                                  stockData.kpi.profitMargins *
                                                  100
                                              ).toFixed(1) + "%"
                                            : "N/A"}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Price Targets Card -->
                        <div
                            class="bg-slate-800/30 rounded-2xl border border-white/5 p-6"
                        >
                            <div class="flex items-center gap-2 mb-4">
                                <TrendingUp class="w-4 h-4 text-amber-400" />
                                <h3 class="text-lg font-bold text-white">
                                    Price Targets
                                </h3>
                            </div>
                            <div class="space-y-3">
                                {#if stockData.targets}
                                    <table class="w-full text-left text-sm">
                                        <thead
                                            class="text-[10px] text-slate-500 uppercase pb-2"
                                        >
                                            <tr>
                                                <th>Period</th>
                                                <th
                                                    class="text-right text-rose-400"
                                                    >Min</th
                                                >
                                                <th
                                                    class="text-right text-blue-400"
                                                    >Avg</th
                                                >
                                                <th
                                                    class="text-right text-emerald-400"
                                                    >Max</th
                                                >
                                            </tr>
                                        </thead>
                                        <tbody class="divide-y divide-white/5">
                                            {#each Object.entries(stockData.targets) as [ptr, val]}
                                                {@const targetVal = val as {
                                                    min: number;
                                                    mean: number;
                                                    max: number;
                                                }}
                                                <tr class="py-2">
                                                    <td
                                                        class="py-2 text-slate-300"
                                                        >{ptr}</td
                                                    >
                                                    <td
                                                        class="py-2 text-right text-rose-400/80"
                                                        >{targetVal.min}</td
                                                    >
                                                    <td
                                                        class="py-2 text-right font-bold text-white"
                                                        >{targetVal.mean}</td
                                                    >
                                                    <td
                                                        class="py-2 text-right text-emerald-400/80"
                                                        >{targetVal.max}</td
                                                    >
                                                </tr>
                                            {/each}
                                        </tbody>
                                    </table>
                                {:else}
                                    <p
                                        class="text-slate-500 text-center py-8 italic"
                                    >
                                        No targets available
                                    </p>
                                {/if}
                            </div>
                        </div>
                    </div>
                {/if}

                <!-- Main Visualization Area (Chart) -->
                <div
                    class="bg-slate-800/30 rounded-2xl border border-white/5 p-6 h-[450px] relative"
                >
                    <StockChart
                        data={getPriceChartData(stockData, loadingPrediction)}
                        title=""
                    />
                    {#if loadingPrediction}
                        <div
                            class="absolute top-4 right-4 flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20 animate-pulse"
                        >
                            <div
                                class="w-2 h-2 rounded-full bg-emerald-400"
                            ></div>
                            Running AI Forecast...
                        </div>
                    {/if}
                </div>

                <!-- Secondary Indicator Area -->
                <div class="grid grid-cols-1 gap-6 mb-6">
                    <div
                        class="bg-slate-800/30 rounded-2xl border border-white/5 p-6"
                    >
                        <div class="flex items-center gap-2 mb-4">
                            <RefreshCw class="w-4 h-4 text-purple-400" />
                            <h3 class="text-lg font-bold text-white">
                                Relative Strength (RSI)
                            </h3>
                        </div>
                        <div class="h-48">
                            <StockChart
                                data={getIndicatorChartData(stockData)}
                                title=""
                            />
                        </div>
                    </div>
                </div>
            </div>
        {:else if loadingStock}
            <div
                class="flex-grow flex items-center justify-center bg-slate-800/30 backdrop-blur-xl border border-white/5 shadow-2xl rounded-2xl p-6"
            >
                <div class="text-center">
                    <div class="relative w-24 h-24 mx-auto mb-6">
                        <div
                            class="absolute inset-0 border-t-4 border-blue-500 rounded-full animate-spin"
                        ></div>
                        <div
                            class="absolute inset-2 border-r-4 border-purple-500 rounded-full animate-spin reverse"
                        ></div>
                        <div
                            class="absolute inset-4 border-b-4 border-cyan-500 rounded-full animate-spin"
                        ></div>
                    </div>
                    <h3 class="text-xl font-bold text-white mb-2">
                        Fetching Market Data
                    </h3>
                    <p class="text-slate-400 animate-pulse">
                        Connecting to European Exchanges...
                    </p>
                </div>
            </div>
        {:else}
            <div
                class="flex-grow flex flex-col items-center justify-center bg-slate-800/30 backdrop-blur-xl border border-white/5 shadow-2xl rounded-2xl p-6 text-center"
            >
                <div
                    class="w-20 h-20 bg-slate-900/50 rounded-full flex items-center justify-center mb-6 shadow-inner ring-1 ring-white/10"
                >
                    <BarChart2 class="h-10 w-10 text-slate-600" />
                </div>
                <h3 class="text-2xl font-bold text-white mb-2">
                    Ready to Analyze
                </h3>
                <p class="text-slate-400 max-w-md">
                    Select a stock from the sidebar to generate real-time
                    technical analysis and simple AI-powered price forecasts.
                </p>
            </div>
        {/if}
    </div>
</div>

<style>
    /* Custom Scrollbar */
    .custom-scrollbar::-webkit-scrollbar {
        width: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    .fade-in {
        animation: fadeIn 0.4s ease-out forwards;
        opacity: 0;
        transform: translateY(10px);
    }

    .delay-100 {
        animation-delay: 0.1s;
    }

    @keyframes fadeIn {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .reverse {
        animation-direction: reverse;
    }
</style>
