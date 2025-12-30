<script lang="ts">
	import { TrendingUp, Sparkles, BarChart3 } from "lucide-svelte";
	import StockSearch from "$lib/components/StockSearch.svelte";
	import { goto } from "$app/navigation";

	interface Props {
		data: {
			stocks: any[];
		};
	}

	let { data }: Props = $props();

	function handleStockSelect(symbol: string) {
		goto(`/analysis?ticker=${symbol}`);
	}
</script>

<div class="min-h-screen">
	<!-- Hero Section -->
	<section class="py-32 px-6 text-center">
		<div class="container max-w-4xl mx-auto space-y-12">
			<div class="space-y-6">
				<div
					class="inline-flex items-center gap-2 px-4 py-2 bg-[#e6f0ff] rounded-full"
				>
					<Sparkles class="text-[#0066ff]" size={16} />
					<span class="text-sm font-semibold text-[#0066ff]"
						>AI-Powered Analysis</span
					>
				</div>

				<h1
					class="text-6xl md:text-7xl font-bold text-[#0a0a0a] leading-tight"
				>
					Smarter investing<br />starts here
				</h1>

				<p class="text-xl text-[#6b7280] max-w-2xl mx-auto">
					Real-time market data and AI predictions for any stock
				</p>
			</div>

			<!-- Search -->
			<div class="max-w-2xl mx-auto">
				<StockSearch onSelect={handleStockSelect} />
			</div>
		</div>
	</section>

	<!-- Popular Stocks -->
	{#if data.stocks && data.stocks.length > 0}
		<section class="py-20 px-6">
			<div class="container max-w-6xl mx-auto">
				<h2 class="text-3xl font-bold text-[#0a0a0a] text-center mb-12">
					Popular Stocks
				</h2>

				<div class="grid grid-cols-2 md:grid-cols-5 gap-6">
					{#each data.stocks as stock}
						<button
							onclick={() => handleStockSelect(stock.symbol)}
							class="bg-white rounded-2xl border border-[#e8eaed] p-6 text-center hover:border-[#0066ff] hover:shadow-lg transition-all"
						>
							<div class="font-bold text-[#0a0a0a] mb-3 text-lg">
								{stock.symbol}
							</div>
							<div class="text-3xl font-bold text-[#0a0a0a] mb-3">
								${stock.price?.toFixed(0) || "N/A"}
							</div>
							<div
								class="{stock.change_percent >= 0
									? 'text-[#00d47e]'
									: 'text-[#ff3b69]'} font-semibold"
							>
								{stock.change_percent >= 0
									? "+"
									: ""}{stock.change_percent?.toFixed(2)}%
							</div>
						</button>
					{/each}
				</div>
			</div>
		</section>
	{/if}

	<!-- Features -->
	<section class="py-32 px-6 bg-white">
		<div class="container max-w-5xl mx-auto">
			<h2 class="text-4xl font-bold text-[#0a0a0a] text-center mb-20">
				Everything you need
			</h2>

			<div class="grid md:grid-cols-3 gap-16">
				<div class="text-center space-y-4">
					<div
						class="w-16 h-16 bg-gradient-to-br from-[#0066ff] to-[#00d47e] rounded-2xl flex items-center justify-center mx-auto"
					>
						<Sparkles class="text-white" size={28} />
					</div>
					<h3 class="text-xl font-bold text-[#0a0a0a]">
						AI Predictions
					</h3>
					<p class="text-[#6b7280]">
						Machine learning models predict future prices
					</p>
				</div>

				<div class="text-center space-y-4">
					<div
						class="w-16 h-16 bg-gradient-to-br from-[#00d47e] to-[#0066ff] rounded-2xl flex items-center justify-center mx-auto"
					>
						<BarChart3 class="text-white" size={28} />
					</div>
					<h3 class="text-xl font-bold text-[#0a0a0a]">
						Technical Analysis
					</h3>
					<p class="text-[#6b7280]">
						Professional indicators and charts
					</p>
				</div>

				<div class="text-center space-y-4">
					<div
						class="w-16 h-16 bg-gradient-to-br from-[#ff3b69] to-[#ffb800] rounded-2xl flex items-center justify-center mx-auto"
					>
						<TrendingUp class="text-white" size={28} />
					</div>
					<h3 class="text-xl font-bold text-[#0a0a0a]">
						Real-Time Data
					</h3>
					<p class="text-[#6b7280]">
						Live market data from Alpha Vantage
					</p>
				</div>
			</div>
		</div>
	</section>

	<!-- CTA -->
	<section class="py-32 px-6">
		<div class="container max-w-3xl mx-auto text-center space-y-8">
			<h2 class="text-5xl font-bold text-[#0a0a0a]">Ready to start?</h2>
			<p class="text-xl text-[#6b7280]">
				Join thousands of investors making smarter decisions
			</p>
			<a
				href="/analysis"
				class="inline-flex items-center gap-2 px-8 py-4 bg-[#0066ff] text-white rounded-full font-semibold hover:bg-[#0052cc] transition-colors"
			>
				<BarChart3 size={20} />
				Start Analyzing
			</a>
		</div>
	</section>
</div>
