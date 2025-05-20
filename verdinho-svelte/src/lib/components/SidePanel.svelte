<script lang="ts">
	import { mapState, type QuadrantData } from '$lib/stores/mapStore.svelte';

	function formatDate(timestamp: number): string {
		return new Date(timestamp).toLocaleString('pt-BR');
	}

	function getRecommendedPlants(quadrants: QuadrantData[]): Record<string, number> {
		const plants: Record<string, number> = {};

		for (const quadrant of quadrants) {
			const plant = quadrant.plantRecommendation.cientific_name;
			if (plant && plant !== 'Erro IA') {
				plants[plant] = (plants[plant] || 0) + 1;
			}
		}

		// Sort by frequency
		return Object.entries(plants)
			.sort((a, b) => b[1] - a[1])
			.slice(0, 5)
			.reduce(
				(acc, [key, value]) => {
					acc[key] = value;
					return acc;
				},
				{} as Record<string, number>
			);
	}
</script>

<div
	class="absolute right-5 top-5 z-1000 max-h-[calc(100vh-40px)] w-[300px] overflow-y-auto rounded-lg bg-white p-5 shadow-md"
	class:opacity-70={mapState.isProcessing}
>
	<h2 class="mb-4 mt-0 text-xl font-semibold text-gray-800">Análise de Reflorestamento</h2>

	{#if mapState.isProcessing}
		<div class="flex min-h-[200px] flex-col items-center justify-center">
			<p>Analisando área selecionada...</p>
			<div
				class="mt-5 h-10 w-10 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"
			></div>
		</div>
	{:else if mapState.quadrants.length > 0}
		<div class="analysis-results">
			<div class="mb-5">
				<h3 class="mb-2 mt-5 text-lg font-medium text-gray-700">Informações da Área</h3>
				<p>
					<strong>Coordenadas:</strong><br />
					Lat: {mapState.selectedArea?.latMin?.toFixed(4)} a {mapState.selectedArea?.latMax?.toFixed(
						4
					)}<br />
					Lon: {mapState.selectedArea?.lonMin?.toFixed(4)} a {mapState.selectedArea?.lonMax?.toFixed(
						4
					)}
				</p>
				<p><strong>Quadrantes analisados:</strong> {mapState.quadrants.length}</p>
				<p>
					<strong>Última análise:</strong>
					{mapState.lastAnalyzedArea ? formatDate(mapState.lastAnalyzedArea.timestamp) : 'N/A'}
				</p>
			</div>

			<!-- <div class="mb-5">
				<h3 class="mb-2 mt-5 text-lg font-medium text-gray-700">Biomas Identificados</h3>
				<ul>
					{#each Object.entries(getBiomeDistribution(mapState.quadrants)) as [biome, count] (biome)}
						<li class="mb-2 rounded-sm bg-gray-100 px-2 py-1">{biome}: {count} quadrantes</li>
					{/each}
				</ul>
			</div> -->

			<div class="mb-5">
				<h3 class="mb-2 mt-5 text-lg font-medium text-gray-700">Plantas Recomendadas</h3>
				<ul>
					{#each Object.entries(getRecommendedPlants(mapState.quadrants)) as [plant, count] (plant)}
						<li class="mb-2 rounded-sm bg-gray-100 px-2 py-1">{plant}: {count} quadrantes</li>
					{/each}
				</ul>
			</div>

			<!-- <div class="mb-5">
				<h3 class="mb-2 mt-5 text-lg font-medium text-gray-700">Distribuição de Necessidade</h3>
				<ul>
					{#each Object.entries(getNeedLevelDistribution(mapState.quadrants)) as [level, count] (level)}
						<li class="mb-2 rounded-sm bg-gray-100 px-2 py-1">{level}: {count} quadrantes</li>
					{/each}
				</ul>
			</div> -->
		</div>
	{:else if mapState.selectedArea}
		<p>Selecione uma área no mapa para análise de reflorestamento.</p>
	{:else}
		<div class="mt-5 border-l-4 border-blue-500 bg-gray-100 p-4">
			<p>Desenhe um retângulo no mapa para analisar área de reflorestamento.</p>
			<p>Use a ferramenta de desenho no canto superior esquerdo do mapa.</p>
		</div>
	{/if}
</div>
