<script lang="ts">
	import type { QuadrantData } from '@/stores/mapStore.svelte';
	import { Droplets, Thermometer, Snowflake, Sun } from '@lucide/svelte';

	let props: {
		quadrant: QuadrantData;
	} = $props();

	const quadrant = $derived(props.quadrant);

	// Climate data with enhanced styling
	const primaryClimateData = [
		{
			label: 'Temperatura Média Anual',
			value: `${quadrant.analyzedAreaData.anual_mean_temperature.toFixed(1)}°C`,
			icon: Thermometer,
			color: 'text-orange-600',
			bgColor: 'bg-orange-50',
			borderColor: 'border-orange-200'
		},
		{
			label: 'Precipitação Média Anual',
			value: `${quadrant.analyzedAreaData.anual_mean_precipitation} mm`,
			icon: Droplets,
			color: 'text-blue-600',
			bgColor: 'bg-blue-50',
			borderColor: 'border-blue-200'
		}
	];

	const secondaryClimateData = [
		{
			label: 'Isotermalidade',
			value: quadrant.analyzedAreaData.isothermality,
			icon: Snowflake,
			color: 'text-cyan-600'
		},
		{
			label: 'Sazonalidade da Temperatura',
			value: quadrant.analyzedAreaData.temperature_seasonality,
			icon: Sun,
			color: 'text-amber-600'
		}
	];
</script>

<div class="space-y-6 pb-4">
	<!-- Primary Climate Metrics -->
	<div class="grid grid-cols-1 gap-4">
		{#each primaryClimateData as item (item.label)}
			<div
				class="group relative overflow-hidden rounded-lg border {item.borderColor} {item.bgColor} p-6 transition-all duration-200 hover:shadow-md"
			>
				<div class="flex items-center gap-4">
					<div class="flex-shrink-0">
						<div
							class="rounded-full bg-white/80 p-3 shadow-sm transition-colors group-hover:bg-white"
						>
							<svelte:component this={item.icon} class="h-6 w-6 {item.color}" />
						</div>
					</div>
					<div class="flex-1">
						<p class="mb-1 text-sm font-medium text-gray-600">
							{item.label}
						</p>
						<p class="text-2xl font-bold text-gray-900">
							{item.value}
						</p>
					</div>
				</div>
				<!-- Subtle background pattern -->
				<div
					class="pointer-events-none absolute inset-0 bg-gradient-to-br from-white via-transparent to-white opacity-5"
				></div>
			</div>
		{/each}
	</div>

	<!-- Secondary Climate Metrics -->
	<div class="space-y-3">
		<h4 class="flex items-center gap-2 text-sm font-semibold text-gray-900">
			<div class="rounded-full bg-gray-100 p-2">
				<Thermometer class="h-4 w-4 text-gray-600" />
			</div>
			Dados Climáticos Adicionais
		</h4>

		<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
			{#each secondaryClimateData as item (item.label)}
				<div
					class="group relative overflow-hidden rounded-lg border border-gray-200 bg-gradient-to-br from-white to-gray-50 p-4 transition-all duration-200 hover:border-gray-300 hover:shadow-md"
				>
					<div class="flex items-start gap-3">
						<div class="flex-shrink-0">
							<div class="rounded-full bg-gray-100 p-2 transition-colors group-hover:bg-gray-200">
								<svelte:component this={item.icon} class="h-4 w-4 {item.color}" />
							</div>
						</div>
						<div class="min-w-0 flex-1">
							<p class="mb-1 text-xs font-medium uppercase tracking-wide text-gray-500">
								{item.label}
							</p>
							<p class="break-words text-sm font-semibold text-gray-900">
								{item.value}
							</p>
						</div>
					</div>
					<!-- Subtle background pattern -->
					<div
						class="pointer-events-none absolute inset-0 bg-gradient-to-br from-transparent via-gray-100 to-transparent opacity-5"
					></div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Climate Summary -->
	<div class="rounded-lg border border-green-200 bg-green-50 p-4">
		<div class="flex items-start gap-3">
			<div class="flex-shrink-0">
				<div class="rounded-full bg-green-100 p-2">
					<Thermometer class="h-4 w-4 text-green-600" />
				</div>
			</div>
			<div>
				<h5 class="mb-1 text-sm font-semibold text-green-900">Resumo Climático</h5>
				<p class="text-sm text-green-700">
					Esta região apresenta condições climáticas adequadas para o cultivo da espécie
					recomendada, com temperatura e precipitação dentro dos parâmetros ideais.
				</p>
			</div>
		</div>
	</div>
</div>
