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
	<div class="min-h-screen relative overflow-x-hidden">
		<nav class="sticky top-0 z-50 border-b border-retro bg-retro-surface">
			<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<div class="flex justify-between h-16">
					<div class="flex items-center">
						<!-- Retro Logo -->
						<div class="flex-shrink-0 flex items-center gap-2">
							<div class="w-8 h-8 border border-retro flex items-center justify-center font-display text-xl bg-retro-accent text-white">
								S
							</div>
							<span class="font-display text-xl tracking-widest uppercase">
								Stock_Pro
							</span>
						</div>
						<!-- Retro Nav Links -->
						<div class="hidden sm:ml-10 sm:flex sm:space-x-8">
							<a href="/" class="text-sm font-mono uppercase tracking-wider py-2 px-3 border border-transparent hover:border-retro hover:bg-retro-accent hover:text-white transition-none">
								Home
							</a>
							<a href="/analysis" class="text-sm font-mono uppercase tracking-wider py-2 px-3 border border-transparent hover:border-retro hover:bg-retro-accent hover:text-white transition-none">
								Analysis
							</a>
							<a href="/compare" class="text-sm font-mono uppercase tracking-wider py-2 px-3 border border-transparent hover:border-retro hover:bg-retro-accent hover:text-white transition-none">
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
