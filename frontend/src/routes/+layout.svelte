<script lang="ts">
	import "../app.css";
	import { page } from "$app/stores";
	import { TrendingUp, LogOut } from "lucide-svelte";
	import Footer from "$lib/components/Footer.svelte";

	let { children, data } = $props();
	let user = $derived(data.user);
	let showUserMenu = $state(false);

	function handleClickOutside(event: MouseEvent) {
		if (showUserMenu) {
			showUserMenu = false;
		}
	}
</script>

<svelte:window onclick={handleClickOutside} />

<div
	class="min-h-screen flex flex-col"
	style="background: var(--color-bg-primary);"
>
	<!-- Navigation -->
	<nav
		style="background: var(--color-bg-elevated); border-bottom: 1px solid var(--color-border);"
	>
		<div class="w-full px-4 md:px-6">
			<div
				class="flex items-center justify-between"
				style="height: 56px;"
			>
				<!-- Logo -->
				<a
					href={user ? "/dashboard" : "/landing"}
					class="flex items-center gap-2"
				>
					<div
						style="width: 32px; height: 32px; background: var(--color-accent); border-radius: var(--radius-lg);"
						class="flex items-center justify-center"
					>
						<TrendingUp style="color: white;" size={18} />
					</div>
					<span
						style="font-size: var(--font-size-lg); font-weight: var(--font-weight-bold); color: var(--color-text-primary);"
						>StockPro</span
					>
				</a>

				<!-- Nav Links & Auth -->
				<div class="flex items-center" style="gap: var(--space-8);">
					{#if user}
						<a
							href="/dashboard"
							style="font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); color: {$page
								.url.pathname === '/dashboard'
								? 'var(--color-accent)'
								: 'var(--color-text-secondary)'}; transition: var(--transition-fast);"
							class="hover-link"
						>
							Dashboard
						</a>
						<a
							href="/analysis"
							style="font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); color: {$page
								.url.pathname === '/analysis'
								? 'var(--color-accent)'
								: 'var(--color-text-secondary)'}; transition: var(--transition-fast);"
							class="hover-link"
						>
							Analysis
						</a>

						<!-- User Menu -->
						<div class="relative">
							<button
								onclick={(e) => {
									e.stopPropagation();
									showUserMenu = !showUserMenu;
								}}
								class="flex items-center transition focus:outline-none"
								style="gap: var(--space-2); opacity: 1; border: none; background: transparent;"
							>
								{#if user.picture}
									<img
										src={user.picture}
										alt={user.name}
										style="width: 28px; height: 28px; border-radius: var(--radius-full);"
									/>
								{:else}
									<div
										style="width: 28px; height: 28px; background: var(--color-accent); border-radius: var(--radius-full); font-size: 10px; font-weight: var(--font-weight-semibold); color: white;"
										class="flex items-center justify-center"
									>
										{user.name?.charAt(0).toUpperCase() ||
											"U"}
									</div>
								{/if}
							</button>

							{#if showUserMenu}
								<div
									style="position: absolute; right: 0; margin-top: var(--space-2); width: 192px; background: var(--color-bg-elevated); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); border: 1px solid var(--color-border); padding: var(--space-1) 0; z-index: 50;"
								>
									<div
										style="padding: var(--space-3) var(--space-4); border-bottom: 1px solid var(--color-border);"
									>
										<p
											style="font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); color: var(--color-text-primary);"
										>
											{user.name}
										</p>
										<p
											style="font-size: var(--font-size-xs); color: var(--color-text-secondary);"
										>
											{user.email}
										</p>
									</div>
									<a
										href="/auth/logout"
										class="flex items-center"
										style="gap: var(--space-2); padding: var(--space-3) var(--space-4); font-size: var(--font-size-sm); color: var(--color-text-primary); text-decoration: none; transition: var(--transition-fast);"
										onmouseenter={(e) =>
											(e.currentTarget.style.background =
												"var(--color-bg-tertiary)")}
										onmouseleave={(e) =>
											(e.currentTarget.style.background =
												"transparent")}
									>
										<LogOut size={16} />
										Sign out
									</a>
								</div>
							{/if}
						</div>
					{:else}
						<a href="/auth/login" class="btn btn-primary">
							Sign in
						</a>
					{/if}
				</div>
			</div>
		</div>
	</nav>

	<!-- Main Content -->
	<main class="flex-1 w-full flex flex-col my-2 py-2">
		{@render children()}
	</main>

	<Footer />
</div>

<style>
	.hover-link:hover {
		color: var(--color-text-primary) !important;
	}
</style>
