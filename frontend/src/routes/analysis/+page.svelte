<script lang="ts">
	import { onMount } from "svelte";
	import { page } from "$app/stores";
	import { ApiService } from "$lib/api";
	import { Indicators } from "$lib/indicators";
	import StockSearch from "$lib/components/StockSearch.svelte";
	import TradingViewWidget from "$lib/components/TradingViewWidget.svelte";
	import NewsCard from "$lib/components/NewsCard.svelte";
	import ErrorState from "$lib/components/ErrorState.svelte";
	import {
		Loader2,
		TrendingUp,
		TrendingDown,
		ExternalLink,
	} from "lucide-svelte";

	let selectedTicker = $state("AAPL");
	let stockInfo = $state<any>(null);
	let history = $state<any[]>([]);
	let predictions = $state<any[]>([]);
	let news = $state<any[]>([]);
	let loading = $state(false);
	let loadingPredict = $state(false);
	let loadingNews = $state(false);
	let error = $state<string | null>(null);

	async function selectStock(ticker: string) {
		selectedTicker = ticker;
		loading = true;
		loadingNews = true;
		error = null;
		predictions = [];
		news = [];

		try {
			const [info, hist] = await Promise.all([
				ApiService.getStockInfo(ticker),
				ApiService.getHistoricalData(ticker, "1mo"),
			]);
			stockInfo = info;
			history = hist;
			loadPredictions(ticker, hist);
			loadNews(ticker);
		} catch (e) {
			error = "Could not load stock data";
		} finally {
			loading = false;
		}
	}

	async function loadPredictions(ticker: string, hist: any[]) {
		loadingPredict = true;
		const res = await ApiService.getPrediction(ticker, hist);
		if (res?.predictions) {
			predictions = res.predictions.map((p: any) => ({
				date: p.Date,
				close: p.PredictedClose,
			}));
		}
		loadingPredict = false;
	}

	async function loadNews(ticker: string) {
		try {
			const response = await fetch(`/api/news?symbol=${ticker}`);
			const data = await response.json();
			news = data.news || [];
		} catch (e) {
			console.error("Error loading news:", e);
		} finally {
			loadingNews = false;
		}
	}

	onMount(() => {
		const urlTicker = $page.url.searchParams.get("ticker");
		if (urlTicker) {
			selectStock(urlTicker);
		} else {
			selectStock("AAPL");
		}
	});

	let volatility = $derived(
		history.length > 0
			? Indicators.calculateVolatility(history.map((h) => h.close))
			: 0,
	);
</script>

<svelte:head>
	<script src="https://s3.tradingview.com/tv.js"></script>
</svelte:head>

<div class="min-h-screen">
	<!-- Search Bar -->
	<div class="bg-white border-b border-[#e8eaed] sticky top-16 z-40">
		<div class="w-full py-4 px-4 md:px-6">
			<StockSearch onSelect={selectStock} />
		</div>
	</div>

	{#if loading}
		<!-- Loading -->
		<div class="w-full px-4 md:px-6 py-32 text-center">
			<Loader2
				class="animate-spin text-[#0066ff] mx-auto mb-4"
				size={48}
			/>
			<p class="text-[#6b7280]">Loading...</p>
		</div>
	{:else if error}
		<!-- Error -->
		<div class="w-full px-4 md:px-6 py-20 flex items-center justify-center">
			<ErrorState
				title="Stock data not found"
				message={error}
				retry={() => selectStock(selectedTicker)}
			/>
		</div>
	{:else if stockInfo}
		<!-- Content -->
		<div class="w-full px-4 md:px-6 py-12 space-y-12 gap-3">
			<!-- Stock Header -->
			<div
				class="flex flex-col md:flex-row md:items-center md:justify-between gap-6 py-2"
			>
				<div class="flex items-center gap-6 py-6">
					{#if stockInfo.logo}
						<img
							src={stockInfo.logo}
							alt={stockInfo.longName}
							class="rounded-lg bg-white shadow-sm p-1 object-contain shrink-0"
							style="width: 8%; height: 8%;"
						/>
					{/if}
					<div>
						<h1
							class="text-4xl font-bold text-[#0a0a0a] mb-2 tracking-tight"
						>
							{stockInfo.longName}
						</h1>
						<div class="flex items-center gap-3 text-[#6b7280]">
							<span
								class="font-mono font-bold text-lg bg-gray-100 px-2 py-0.5 rounded"
								>{selectedTicker}</span
							>
							<span class="text-sm">{stockInfo.exchange}</span>
							{#if stockInfo.website}
								<span class="text-gray-300">|</span>
								<a
									href={stockInfo.website}
									target="_blank"
									rel="noopener noreferrer"
									class="flex items-center gap-1 hover:text-[#0066ff] transition-colors text-sm font-medium"
								>
									Website
									<ExternalLink size={14} />
								</a>
							{/if}
						</div>
					</div>
				</div>
				<div class="text-left md:text-right">
					<div class="flex items-baseline gap-4 md:justify-end">
						<div
							class="text-6xl font-bold text-[#0a0a0a] tracking-tight"
						>
							${stockInfo.price?.toLocaleString()}
						</div>
						<div
							class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg {stockInfo.change >=
							0
								? 'bg-green-100/50 text-[#00d47e]'
								: 'bg-red-100/50 text-[#ff3b69]'} font-bold text-xl self-center"
						>
							{#if stockInfo.change >= 0}
								<TrendingUp size={20} />
							{:else}
								<TrendingDown size={20} />
							{/if}
							{stockInfo.change >= 0
								? "+"
								: ""}{stockInfo.change?.toFixed(2)} ({stockInfo.change_percent?.toFixed(
								2,
							)}%)
						</div>
					</div>
					<div class="text-sm text-gray-500 font-medium mt-2">
						Real-time price • USD
					</div>
				</div>
			</div>

			<!-- Main Content Stack -->
			<div class="space-y-12 gap-5">
				<!-- Key Indicators Bar -->
				<div class="grid grid-cols-2 md:grid-cols-4 gap-6">
					<div
						class="bg-white rounded-xl border border-[#e8eaed] p-4"
					>
						<span class="text-sm text-[#6b7280] block mb-1"
							>Market Cap</span
						>
						<span class="text-lg font-bold text-[#0a0a0a]"
							>${(stockInfo.marketCap / 1e9).toFixed(2)}B</span
						>
					</div>
					<div
						class="bg-white rounded-xl border border-[#e8eaed] p-4"
					>
						<span class="text-sm text-[#6b7280] block mb-1"
							>Volatility</span
						>
						<span class="text-lg font-bold text-[#0a0a0a]"
							>{(volatility * 100).toFixed(2)}%</span
						>
					</div>
					<div
						class="bg-white rounded-xl border border-[#e8eaed] p-4"
					>
						<span class="text-sm text-[#6b7280] block mb-1"
							>Sector</span
						>
						<span
							class="text-lg font-bold text-[#0a0a0a] truncate"
							title={stockInfo.sector}>{stockInfo.sector}</span
						>
					</div>
					<div
						class="bg-white rounded-xl border border-[#e8eaed] p-4"
					>
						<span class="text-sm text-[#6b7280] block mb-1"
							>Exchange</span
						>
						<span class="text-lg font-bold text-[#0a0a0a]"
							>{stockInfo.exchange}</span
						>
					</div>
				</div>

				<!-- TradingView Chart -->
				<div
					class="bg-white rounded-2xl border border-[#e8eaed] overflow-hidden"
					style="margin-bottom: 1rem; margin-top: 1rem;"
				>
					<TradingViewWidget symbol={selectedTicker} height={600} />
				</div>

				<!-- About & Details -->
				<div class="bg-white rounded-2xl border border-[#e8eaed] p-6">
					<div class="flex flex-col md:flex-row gap-8">
						<div class="flex-1">
							<h3 class="text-lg font-bold text-[#0a0a0a] mb-3">
								About {stockInfo.longName}
							</h3>
							<p class="text-sm text-[#6b7280] leading-relaxed">
								{stockInfo.description}
							</p>
						</div>
						<div
							class="md:w-64 space-y-4 shrink-0 border-l border-[#e8eaed] md:pl-8 mt-4 md:mt-0 pt-4 md:pt-0 border-t md:border-t-0"
						>
							<div>
								<span
									class="text-xs font-medium text-[#6b7280] uppercase tracking-wider block mb-1"
									>IPO Date</span
								>
								<span class="font-medium text-[#0a0a0a]"
									>{stockInfo.ipo}</span
								>
							</div>
							<div>
								<span
									class="text-xs font-medium text-[#6b7280] uppercase tracking-wider block mb-1"
									>Industry</span
								>
								<span class="font-medium text-[#0a0a0a]"
									>{stockInfo.industry}</span
								>
							</div>
							<div>
								<span
									class="text-xs font-medium text-[#6b7280] uppercase tracking-wider block mb-1"
									>Currency</span
								>
								<span class="font-medium text-[#0a0a0a]"
									>{stockInfo.currency}</span
								>
							</div>
						</div>
					</div>
				</div>

				<!-- News -->
				<div class="space-y-4">
					<h2 class="text-2xl font-bold text-gray-900">
						Latest News regarding {stockInfo.longName}
					</h2>
					{#if loadingNews}
						<div class="text-center py-8">
							<Loader2
								class="animate-spin text-[#0066ff] mx-auto"
								size={32}
							/>
						</div>
					{:else}
						<NewsCard {news} />
					{/if}
				</div>
			</div>
		</div>
	{:else}
		<!-- Empty State -->
		<div class="w-full px-4 md:px-6 py-32 text-center">
			<h2 class="text-3xl font-bold text-[#0a0a0a] mb-3">
				Search for a stock
			</h2>
			<p class="text-[#6b7280]">Enter a symbol above to view analysis</p>
		</div>
	{/if}
</div>
