<script lang="ts">
    import { TrendingUp, TrendingDown } from "lucide-svelte";
    import type { MarketIndex } from "../services/api";

    let { index } = $props<{ index: MarketIndex }>();
</script>

<div class="bg-white overflow-hidden shadow rounded-lg p-5">
    <div class="flex items-center">
        <div class="flex-shrink-0">
            <!-- Icon based on logic could go here, or just generic -->
            <div class="rounded-md bg-blue-500 p-3">
                <span class="text-white font-bold text-lg"
                    >{index.ticker.substring(1, 3)}</span
                >
            </div>
        </div>
        <div class="ml-5 w-0 flex-1">
            <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                    {index.name}
                </dt>
                <dd>
                    <div class="text-lg font-medium text-gray-900">
                        {index.price}
                        {index.currency}
                    </div>
                </dd>
                <dd class="flex items-center">
                    {#if index.change >= 0}
                        <TrendingUp class="w-4 h-4 text-green-500 mr-1" />
                        <span class="text-sm font-semibold text-green-600"
                            >+{index.change_percent}%</span
                        >
                    {:else}
                        <TrendingDown class="w-4 h-4 text-red-500 mr-1" />
                        <span class="text-sm font-semibold text-red-600"
                            >{index.change_percent}%</span
                        >
                    {/if}
                    <span class="text-xs text-gray-400 ml-2"
                        >({index.change})</span
                    >
                </dd>
            </dl>
        </div>
    </div>
</div>
