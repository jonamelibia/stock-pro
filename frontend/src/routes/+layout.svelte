<script lang="ts">
	import "../app.css";
	import favicon from "$lib/assets/favicon.svg";
	import { page } from "$app/stores";

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if $page.url.pathname === "/"}
	{@render children()}
{:else}
	<div
		class="min-h-screen bg-slate-900 text-white font-sans relative overflow-x-hidden"
	>
		<!-- Global Background Effects -->
		<div
			class="fixed top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none"
		>
			<div
				class="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[128px] animate-pulse"
			></div>
			<div
				class="absolute bottom-[-10%] left-[-5%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[128px] animate-pulse delay-1000"
			></div>
		</div>

		<nav
			class="relative z-50 border-b border-white/5 bg-slate-900/50 backdrop-blur-md sticky top-0"
		>
			<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<div class="flex justify-between h-16">
					<div class="flex items-center">
						<div class="flex-shrink-0 flex items-center gap-2">
							<div
								class="w-8 h-8 rounded bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20"
							>
								S
							</div>
							<span
								class="font-bold text-xl bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400"
							>
								Stock Pro
							</span>
						</div>
						<div class="hidden sm:ml-10 sm:flex sm:space-x-8">
							<a
								href="/"
								class="border-transparent text-slate-300 hover:border-blue-500 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
							>
								Home
							</a>
							<a
								href="/analysis"
								class="border-transparent text-slate-300 hover:border-blue-500 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
							>
								Analysis
							</a>
							<a
								href="/compare"
								class="border-transparent text-slate-300 hover:border-blue-500 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
							>
								Compare
							</a>
						</div>
					</div>
				</div>
			</div>
		</nav>

		<main class="relative z-10 max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
			{@render children()}
		</main>
	</div>
{/if}
