<script lang="ts">
	import type { QuadrantData } from '@/stores/mapStore.svelte';
	import { MapPin, Globe, Navigation } from '@lucide/svelte';

	let props: {
		quadrant: QuadrantData;
	} = $props();

	const quadrant = $derived(props.quadrant);

	// Format coordinates for better display
	const formatCoordinate = (coord: number, type: 'lat' | 'lon') => {
		const direction = type === 'lat' ? (coord >= 0 ? 'N' : 'S') : coord >= 0 ? 'E' : 'W';
		return `${Math.abs(coord).toFixed(6)}° ${direction}`;
	};

	const locationData = [
		{
			label: 'Latitude',
			value: formatCoordinate(quadrant.lat, 'lat'),
			rawValue: quadrant.lat,
			icon: Navigation,
			color: 'text-blue-600'
		},
		{
			label: 'Longitude',
			value: formatCoordinate(quadrant.lon, 'lon'),
			rawValue: quadrant.lon,
			icon: Globe,
			color: 'text-green-600'
		}
	];
</script>

<div class="space-y-6 pb-4">
	<!-- Coordinates Section -->
	<div class="space-y-3">
		<div class="flex items-center gap-2">
			<div class="rounded-full bg-blue-100 p-2">
				<MapPin class="h-4 w-4 text-blue-600" />
			</div>
			<h4 class="text-sm font-semibold text-gray-900">Coordenadas Geográficas</h4>
		</div>

		<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
			{#each locationData as item (item.label)}
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
							<p class="font-mono text-sm font-semibold text-gray-900">
								{item.value}
							</p>
							<p class="mt-1 font-mono text-xs text-gray-500">
								{item.rawValue}
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

	<!-- Map Section -->
	<div class="space-y-3">
		<div class="flex items-center gap-2">
			<div class="rounded-full bg-green-100 p-2">
				<Globe class="h-4 w-4 text-green-600" />
			</div>
			<h4 class="text-sm font-semibold text-gray-900">Visualização no Mapa</h4>
		</div>

		<div
			class="relative aspect-video overflow-hidden rounded-lg border border-gray-200 bg-gray-100 shadow-sm"
		>
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

			<!-- Loading state overlay -->
			<div
				class="pointer-events-none absolute inset-0 flex items-center justify-center bg-gray-100 opacity-0 transition-opacity duration-300"
				id="map-loading"
			>
				<div class="flex flex-col items-center gap-2">
					<MapPin class="h-8 w-8 animate-pulse text-gray-400" />
					<span class="text-sm text-gray-500">Carregando mapa...</span>
				</div>
			</div>
		</div>
	</div>
</div>
