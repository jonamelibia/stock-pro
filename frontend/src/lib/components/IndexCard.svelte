<script lang="ts">
    import { TrendingUp, TrendingDown } from "lucide-svelte";
    import type { MarketIndex } from "../services/api";

    let { index } = $props<{ index: MarketIndex }>();
</script>

<div
    class="bg-white border border-retro p-5 group hover:bg-retro-surface transition-colors"
>
    <div class="flex items-center">
        <div class="flex-shrink-0">
            <!-- Icon based on logic could go here, or just generic -->
            <div
                class="border border-retro p-3 bg-retro-accent text-white font-mono font-bold text-lg flex items-center justify-center w-12 h-12"
            >
                <span>{index.ticker.substring(1, 3)}</span>
            </div>
        </div>
        <div class="ml-5 w-0 flex-1">
            <dl>
                <dt
                    class="text-sm font-mono text-retro-fg truncate uppercase tracking-tight"
                >
                    {index.name}
                </dt>
                <dd>
                    <div class="text-lg font-display text-retro-fg">
                        {index.price.toFixed(2)}
                        <span class="text-sm font-mono">{index.currency}</span>
                    </div>
                </dd>
                <dd class="flex items-center mt-1">
                    {#if index.change >= 0}
                        <TrendingUp class="w-4 h-4 text-retro-fg mr-1" />
                        <span class="text-sm font-mono font-bold text-retro-fg"
                            >+{index.change_percent}%</span
                        >
                    {:else}
                        <TrendingDown class="w-4 h-4 text-retro-accent mr-1" />
                        <span
                            class="text-sm font-mono font-bold text-retro-accent"
                            >{index.change_percent}%</span
                        >
                    {/if}
                    <span class="text-xs font-mono text-gray-500 ml-2"
                        >({index.change})</span
                    >
                </dd>
            </dl>
        </div>
    </div>
</div>
