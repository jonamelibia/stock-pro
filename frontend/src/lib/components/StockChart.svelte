<script lang="ts">
	import { onMount, onDestroy } from "svelte";
	import Chart from "chart.js/auto";
	import "chartjs-adapter-date-fns";

	let { data, title = "Stock Price", color = "#0066ff" } = $props();

	let chartCanvas: HTMLCanvasElement;
	let chart: Chart;

	$effect(() => {
		if (chart) {
			chart.data.labels = data.map((d: any) => d.date);
			chart.data.datasets[0].data = data.map((d: any) => d.close);
			chart.update();
		}
	});

	onMount(() => {
		chart = new Chart(chartCanvas, {
			type: "line",
			data: {
				labels: data.map((d: any) => d.date),
				datasets: [
					{
						label: title,
						data: data.map((d: any) => d.close),
						borderColor: color,
						backgroundColor: (context) => {
							const ctx = context.chart.ctx;
							const gradient = ctx.createLinearGradient(
								0,
								0,
								0,
								400,
							);
							gradient.addColorStop(0, color + "22");
							gradient.addColorStop(1, color + "00");
							return gradient;
						},
						fill: true,
						tension: 0.4,
						pointRadius: 0,
						pointHitRadius: 10,
						borderWidth: 2,
					},
				],
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				layout: { padding: { top: 10, bottom: 10 } },
				plugins: {
					legend: { display: false },
					tooltip: {
						mode: "index",
						intersect: false,
						backgroundColor: "rgba(255, 255, 255, 0.95)",
						titleColor: "#6b7280",
						titleFont: { family: "Inter", size: 11, weight: "600" },
						bodyColor: "#0a0a0a",
						bodyFont: { family: "Inter", size: 14, weight: "700" },
						borderColor: "#e8eaed",
						borderWidth: 1,
						padding: 12,
						displayColors: false,
						callbacks: {
							label: (context) =>
								`$${context.parsed.y.toLocaleString()}`,
						},
					},
				},
				scales: {
					x: {
						type: "time",
						time: { unit: "day" },
						grid: { display: false },
						ticks: {
							color: "#9ca3af",
							font: { family: "Inter", size: 10 },
							maxRotation: 0,
						},
					},
					y: {
						grid: { color: "#f7f8fa", drawTicks: false },
						border: { display: false },
						ticks: {
							color: "#9ca3af",
							font: { family: "Inter", size: 10 },
							callback: (value) => "$" + value,
						},
					},
				},
			},
		});
	});

	onDestroy(() => {
		if (chart) chart.destroy();
	});
</script>

<div class="h-full w-full">
	<canvas bind:this={chartCanvas}></canvas>
</div>
