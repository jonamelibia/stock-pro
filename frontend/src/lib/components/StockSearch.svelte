<script lang="ts">
    import { ApiService } from "$lib/api";
    import { Search } from "lucide-svelte";

    let searchQuery = $state("");
    let searchResults = $state<any[]>([]);
    let isSearching = $state(false);
    let showResults = $state(false);

    interface Props {
        onSelect?: (symbol: string) => void;
        placeholder?: string;
    }

    let {
        onSelect,
        placeholder = "Search stocks (e.g., AAPL, MSFT, TSLA)...",
    }: Props = $props();

    let searchTimeout: ReturnType<typeof setTimeout>;

    async function handleSearch() {
        if (searchQuery.length < 1) {
            searchResults = [];
            showResults = false;
            return;
        }

        isSearching = true;
        clearTimeout(searchTimeout);

        searchTimeout = setTimeout(async () => {
            try {
                const data = await ApiService.searchStocks(searchQuery);
                searchResults = data.results || [];
                showResults = true;
            } catch (e) {
                console.error("Search error:", e);
                searchResults = [];
            } finally {
                isSearching = false;
            }
        }, 300);
    }

    function selectStock(symbol: string) {
        searchQuery = symbol;
        showResults = false;
        if (onSelect) {
            onSelect(symbol);
        }
    }

    function handleBlur() {
        setTimeout(() => {
            showResults = false;
        }, 200);
    }
</script>

<div class="relative w-full">
    <div class="relative">
        <input
            type="text"
            bind:value={searchQuery}
            oninput={handleSearch}
            onblur={handleBlur}
            onfocus={() => searchQuery.length > 0 && (showResults = true)}
            class="w-full px-4 py-3 rounded-xl focus:outline-none transition-all shadow-sm"
            style="
				background: var(--color-input-bg);
				border: 1px solid var(--color-border);
				color: var(--color-text-primary);
			"
            placeholder="Search symbol..."
        />
        {#if isSearching}
            <div class="absolute right-4 top-1/2 -translate-y-1/2">
                <div
                    class="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"
                ></div>
            </div>
        {/if}
    </div>

    {#if showResults && searchResults.length > 0}
        <div
            class="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-[400px] overflow-y-auto z-50"
        >
            {#each searchResults as result}
                <button
                    onclick={() => selectStock(result.symbol)}
                    class="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-b-0"
                >
                    <div class="flex items-center justify-between">
                        <div class="flex-1 min-w-0">
                            <div class="font-semibold text-gray-900">
                                {result.symbol}
                            </div>
                            <div class="text-sm text-gray-600 truncate">
                                {result.name}
                            </div>
                        </div>
                        <div class="text-xs text-gray-500 ml-4 flex-shrink-0">
                            {result.region} · {result.type}
                        </div>
                    </div>
                </button>
            {/each}
        </div>
    {/if}

    {#if showResults && searchResults.length === 0 && searchQuery.length > 0 && !isSearching}
        <div
            class="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg p-4 z-50"
        >
            <p class="text-gray-600 text-center text-sm">
                No results found for "{searchQuery}"
            </p>
        </div>
    {/if}
</div>
