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
                    maintainAspectRatio: false,
                    elements: {
                        line: {
                            borderColor: "#D71921", // Retro Accent
                            borderWidth: 2,
                            tension: 0, // Sharp lines
                        },
                        point: {
                            backgroundColor: "#111", // Retro Foreground
                            radius: 0,
                            hoverRadius: 6,
                        },
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false, // Clean look
                                drawBorder: true,
                                borderColor: "#111",
                            },
                            ticks: {
                                font: {
                                    family: "'Space Mono', monospace",
                                },
                                color: "#111",
                            },
                        },
                        y: {
                            grid: {
                                color: "#e5e5e5", // Subtle grid
                                borderDash: [2, 2], // Dotted grid
                                drawBorder: true,
                                borderColor: "#111",
                            },
                            ticks: {
                                font: {
                                    family: "'Space Mono', monospace",
                                },
                                color: "#111",
                            },
                        },
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: title,
                            font: {
                                family: "'DotGothic16', monospace",
                                size: 16,
                            },
                            color: "#111",
                            padding: 20,
                        },
                        legend: {
                            labels: {
                                font: {
                                    family: "'Space Mono', monospace",
                                },
                                color: "#111",
                            },
                        },
                        tooltip: {
                            mode: "index",
                            intersect: false,
                            backgroundColor: "#111",
                            titleFont: { family: "'Space Mono', monospace" },
                            bodyFont: { family: "'Space Mono', monospace" },
                            cornerRadius: 0, // Sharp corners
                            displayColors: false,
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
