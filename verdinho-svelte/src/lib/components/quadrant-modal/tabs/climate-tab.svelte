<script lang="ts">
	import type { QuadrantData } from '@/stores/mapStore.svelte';
	import { Droplets, Thermometer } from '@lucide/svelte';

	let props: {
		quadrant: QuadrantData;
	} = $props();

	const quadrant = $derived(props.quadrant);
</script>

<div class="space-y-4">
	<div class="grid grid-cols-2 gap-4">
		<div class="col-span-2 flex items-center rounded-lg border border-green-100 bg-green-50 p-3">
			<Thermometer class="mr-3 h-10 w-10 text-green-600" />
			<div>
				<p class="text-muted-foreground text-sm font-medium">Temperatura Média Anual</p>
				<p class="text-xl font-semibold">
					{quadrant.analyzedAreaData.anual_mean_temperature.toFixed(0)}°C
				</p>
			</div>
		</div>
		<div class="col-span-2 flex items-center rounded-lg border border-blue-100 bg-blue-50 p-3">
			<Droplets class="mr-3 h-10 w-10 text-blue-600" />
			<div>
				<p class="text-muted-foreground text-sm font-medium">Precipitação Média Anual</p>
				<p class="text-xl font-semibold">
					{quadrant.analyzedAreaData.anual_mean_precipitation} mm
				</p>
			</div>
		</div>
		<div>
			<p class="text-muted-foreground text-sm font-medium">Isotermalidade</p>
			<p class="text-base">
				{quadrant.analyzedAreaData.isothermality}
			</p>
		</div>
		<div>
			<p class="text-muted-foreground text-sm font-medium">Sazonalidade da Temperatura</p>
			<p class="text-base">
				{quadrant.analyzedAreaData.temperature_seasonality}
			</p>
		</div>
	</div>
</div>
