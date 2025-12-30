<script lang="ts">
	let { targets } = $props();
</script>

{#if targets}
	<div class="flex flex-col gap-6">
		{#each Object.entries(targets) as [period, values]}
			<div class="border-b border-white/5 pb-6 last:border-0 last:pb-0">
				<span class="text-[10px] uppercase font-black tracking-[0.2em] text-text-secondary">{period}</span>
				<div class="mt-4">
					<div class="flex justify-between items-baseline mb-2">
						<span class="text-[11px] font-bold text-text-tertiary">PROYECCIÓN</span>
						<span class="font-mono text-sm font-bold text-accent">${values.max.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</span>
					</div>
					<div class="w-full h-[3px] bg-white/5 rounded-full overflow-hidden relative">
						<div class="absolute inset-y-0 left-0 right-0 bg-linear-to-r from-error/40 via-accent/40 to-accent/40 opacity-30"></div>
						<div class="absolute inset-y-0 left-1/2 w-px bg-white/20 z-10"></div>
					</div>
					<div class="flex justify-between items-baseline mt-2">
						<span class="text-[11px] font-bold text-text-tertiary uppercase">Riesgo</span>
						<span class="font-mono text-sm font-bold text-error">${values.min.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</span>
					</div>
				</div>
			</div>
		{/each}
	</div>
{/if}
