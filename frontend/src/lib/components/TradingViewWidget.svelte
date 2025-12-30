<script lang="ts">
    import { onMount } from "svelte";

    interface Props {
        symbol: string;
        theme?: "light" | "dark";
        height?: number;
    }

    let { symbol, theme = "light", height = 500 }: Props = $props();
    let container: HTMLDivElement;

    onMount(() => {
        // Create TradingView widget script
        const script = document.createElement("script");
        script.src = "https://s3.tradingview.com/tv.js";
        script.async = true;
        script.onload = () => {
            if (typeof TradingView !== "undefined") {
                new TradingView.widget({
                    autosize: true,
                    symbol: symbol,
                    interval: "D",
                    timezone: "Etc/UTC",
                    theme: theme,
                    style: "1",
                    locale: "en",
                    toolbar_bg: "#f1f3f6",
                    enable_publishing: false,
                    allow_symbol_change: true,
                    container_id: "tradingview_widget",
                    studies: [
                        "RSI@tv-basicstudies",
                        "MASimple@tv-basicstudies",
                    ],
                    show_popup_button: true,
                    popup_width: "1000",
                    popup_height: "650",
                });
            }
        };

        container.appendChild(script);

        return () => {
            // Cleanup
            if (container) {
                container.innerHTML = "";
            }
        };
    });
</script>

<div
    bind:this={container}
    id="tradingview_widget"
    style="height: {height}px;"
></div>
