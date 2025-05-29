<script lang="ts">
	import Map from '$lib/components/Map.svelte';
	import SidePanel from '$lib/components/SidePanel.svelte';
	import QuadrantModal from '$lib/components/quadrant-modal/quadrant-modal.svelte';
	import MapFooter from '@/components/map-footer.svelte';

	let isLoading = $state(true);

	$effect(() => {
		// Set loading to false after a brief delay
		setTimeout(() => {
			isLoading = false;
		}, 1000); // Allow time for dynamic imports to complete
	});
</script>

<div class="relative h-full w-full">
	{#if isLoading}
		<div class="flex h-screen flex-col items-center justify-center bg-gray-100">
			<div
				class="mb-5 h-12 w-12 animate-spin rounded-full border-4 border-blue-500 border-t-transparent border-opacity-75"
			></div>
			<p class="text-gray-700">Carregando o mapa...</p>
		</div>
	{:else}
		<main class="h-full w-full">
			<Map />
			<MapFooter />
			<SidePanel />
			<QuadrantModal />
		</main>
	{/if}
</div>
