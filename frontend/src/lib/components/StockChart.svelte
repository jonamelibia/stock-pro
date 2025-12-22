<script lang="ts">
    import { onMount } from "svelte";
    import Chart from "chart.js/auto";

    let { data, title } = $props<{ data: any; title: string }>();
    let canvas: HTMLCanvasElement;
    let chart: Chart;

    onMount(() => {
        if (canvas) {
            chart = new Chart(canvas, {
                type: "line",
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: title,
                        },
                        tooltip: {
                            mode: "index",
                            intersect: false,
                        },
                    },
                    interaction: {
                        mode: "nearest",
                        axis: "x",
                        intersect: false,
                    },
                },
            });
        }

        return () => {
            if (chart) chart.destroy();
        };
    });

    // Watch for data changes
    $effect(() => {
        if (chart && data) {
            chart.data = data;
            chart.update();
        }
    });
</script>

<div class="relative h-96 w-full">
    <canvas bind:this={canvas}></canvas>
</div>
