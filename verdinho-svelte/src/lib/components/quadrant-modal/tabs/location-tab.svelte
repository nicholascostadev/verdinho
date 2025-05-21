<script lang="ts">
	import type { QuadrantData } from '@/stores/mapStore.svelte';

	let props: {
		quadrant: QuadrantData;
	} = $props();

	const quadrant = $derived(props.quadrant);
</script>

<div class="space-y-4">
	<div class="rounded-lg bg-slate-50 p-4">
		<div class="grid grid-cols-2 gap-4">
			<div>
				<p class="text-muted-foreground text-sm font-medium">Latitude</p>
				<p class="font-mono text-base">{quadrant.lat}</p>
			</div>
			<div>
				<p class="text-muted-foreground text-sm font-medium">Longitude</p>
				<p class="font-mono text-base">{quadrant.lon}</p>
			</div>
		</div>
	</div>

	<div class="relative aspect-video overflow-hidden rounded-lg border bg-slate-100">
		<div class="absolute inset-0 flex items-center justify-center">
			<iframe
				title="Mapa da localização"
				frameborder="0"
				scrolling="no"
				marginheight="0"
				marginwidth="0"
				src="https://maps.google.com/maps?q={quadrant.lat},{quadrant.lon}&hl=pt-BR&z=14&amp;output=embed"
				class="h-full w-full"
			>
			</iframe>
			<br />
			<!-- <MapPin class="h-8 w-8 text-slate-400" />
			<span class="ml-2 text-sm text-slate-500">Mapa da localização</span> -->
		</div>
	</div>

	<div>
		<h4 class="text-muted-foreground mb-2 text-sm font-medium">Informações do terreno</h4>
		<ul class="list-disc space-y-1 pl-5 text-sm">
			<li>Altitude: 45m acima do nível do mar</li>
			<li>Tipo de solo: Arenoso</li>
			<li>Inclinação: Leve (5-10%)</li>
			<li>Exposição solar: Alta</li>
		</ul>
	</div>
</div>
