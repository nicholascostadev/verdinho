<script lang="ts">
	import { Separator } from '@/components/ui/separator';
	import type { QuadrantData } from '@/stores/mapStore.svelte';
	import { Leaf, TreePine, Flower, Dna } from '@lucide/svelte';
	import PlantCharacteristics from '../plant-characteristics.svelte';
	import PlantGallery from '../plant-gallery.svelte';

	let props: {
		quadrant: QuadrantData;
	} = $props();

	const quadrant = $derived(props.quadrant);

	// Taxonomy data with icons
	const taxonomyData = $derived([
		{
			label: 'Classe',
			value: quadrant.plantRecommendation.class,
			icon: TreePine,
			color: 'text-emerald-600'
		},
		{
			label: 'Família',
			value: quadrant.plantRecommendation.family,
			icon: Leaf,
			color: 'text-green-600'
		},
		{
			label: 'Ordem',
			value: quadrant.plantRecommendation.order,
			icon: Flower,
			color: 'text-lime-600'
		},
		{
			label: 'Gênero',
			value: quadrant.plantRecommendation.gender,
			icon: Dna,
			color: 'text-teal-600'
		}
	]);
</script>

<div class="max-w-full space-y-6 pb-4">
	<div class="grid w-full gap-8 md:grid-cols-2">
		<div class="max-h-[350px]">
			<PlantGallery cientificName={quadrant.plantRecommendation.cientific_name} />
		</div>

		<!-- Taxonomy Grid -->
		<div class="grid h-fit max-w-full gap-4 sm:grid-cols-2">
			{#each taxonomyData as item (item.label)}
				<div
					class="group relative max-w-full overflow-hidden rounded-lg border border-gray-200 bg-gradient-to-br from-white to-gray-50 p-4 transition-all duration-200 hover:border-gray-300 hover:shadow-md"
				>
					<div class="flex items-start gap-3">
						<div class="">
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

	<Separator />

	<!-- Characteristics Section -->
	<PlantCharacteristics cientificName={quadrant.plantRecommendation.cientific_name} />
</div>
