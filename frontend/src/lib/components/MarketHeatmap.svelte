<script lang="ts">
    import { onMount } from "svelte";

    interface Props {
        stocks: any[];
    }

    let { stocks }: Props = $props();
    let container: HTMLDivElement;

    onMount(() => {
        // Create TradingView Market Heatmap
        const script = document.createElement("script");
        script.src =
            "https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js";
        script.async = true;
        script.innerHTML = JSON.stringify({
            exchanges: [],
            dataSource: "SPX500",
            grouping: "sector",
            blockSize: "market_cap_basic",
            blockColor: "change",
            locale: "en",
            symbolUrl: "",
            colorTheme: "light",
            hasTopBar: false,
            isDataSetEnabled: false,
            isZoomEnabled: true,
            hasSymbolTooltip: true,
            width: "100%",
            height: "100%",
        });

        container.appendChild(script);

        return () => {
            if (container) {
                container.innerHTML = "";
            }
        };
    });
</script>

<div
    class="bg-white rounded-2xl border border-[#e8eaed] overflow-hidden"
    style="height: 600px;"
>
    <div
        bind:this={container}
        class="tradingview-widget-container"
        style="height: 100%; width: 100%;"
    >
        <div class="tradingview-widget-container__widget"></div>
    </div>
</div>
