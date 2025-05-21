<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { quadrantModalStore } from '$lib/stores/quadrant-modal-store.svelte';
	import { Badge } from '../ui/badge';
	import { Button } from '../ui/button';
	import { Leaf, Thermometer, MapPin } from '@lucide/svelte';
	import * as Tabs from '$lib/components/ui/tabs';
	import ClimateTab from './tabs/climate-tab.svelte';
	import TaxonomyTab from './tabs/taxonomy-tab.svelte';
	import LocationTab from './tabs/location-tab.svelte';

	let activeTab: 'taxonomy' | 'climate' | 'location' = $state('taxonomy');

	$effect(() => {
		if (quadrantModalStore.isOpen) {
			activeTab = 'taxonomy';
		}
	});
</script>

{#if quadrantModalStore.quadrant}
	<Dialog.Root bind:open={quadrantModalStore.isOpen}>
		<Dialog.Content class="overflow-clip p-0 sm:max-w-3xl">
			<Tabs.Root bind:value={activeTab}>
				<Dialog.Header class="bg-green-50 px-6 pt-6">
					<div class="flex items-start justify-between">
						<div>
							<Badge variant="outline" class="mb-2 bg-green-100 text-green-800">
								Planta Recomendada
							</Badge>
							<Dialog.Title class="text-2xl font-bold text-green-900"
								>{quadrantModalStore.quadrant.plantRecommendation.cientific_name}</Dialog.Title
							>
							<Dialog.Description class="mt-1 text-green-700">
								Informações do quadrante para recomendação de plantio
							</Dialog.Description>
						</div>
					</div>

					<Tabs.List class="bg-transparent shadow-none">
						<Tabs.Trigger
							value="taxonomy"
							class="rounded-none border-0 border-b-2 px-4 text-green-600 data-[state=active]:border-green-600 data-[state=active]:bg-transparent data-[state=active]:text-green-800 data-[state=active]:shadow-none"
						>
							<Leaf class="mr-2 h-4 w-4" />
							Taxonomia
						</Tabs.Trigger>
						<Tabs.Trigger
							value="climate"
							class="rounded-none border-0 border-b-2 px-4 text-green-600 data-[state=active]:border-green-600 data-[state=active]:bg-transparent data-[state=active]:text-green-800 data-[state=active]:shadow-none"
						>
							<Thermometer class="mr-2 h-4 w-4" />
							Clima
						</Tabs.Trigger>
						<Tabs.Trigger
							value="location"
							class="rounded-none border-0 border-b-2 px-4 text-green-600 data-[state=active]:border-green-600 data-[state=active]:bg-transparent data-[state=active]:text-green-800 data-[state=active]:shadow-none"
						>
							<MapPin class="mr-2 h-4 w-4" />
							Localização
						</Tabs.Trigger>
					</Tabs.List>
				</Dialog.Header>

				<div class="grid grid-cols-1 gap-6 p-6 md:grid-cols-3">
					<div class="flex flex-col items-center justify-center md:col-span-1">
						<div
							class="relative aspect-square w-full overflow-hidden rounded-lg border border-green-100 bg-green-50"
						>
							<!-- <img
							src={data.imageUrl || '/placeholder.svg?height=200&width=200'}
							alt={data.scientificName}
							fill
							class="object-cover"
						/> -->
						</div>
						<Button variant="outline" class="mt-4 w-full">Ver detalhes completos</Button>
					</div>

					<div class="md:col-span-2">
						<Tabs.Content value="taxonomy">
							<TaxonomyTab quadrant={quadrantModalStore.quadrant} />
						</Tabs.Content>

						<Tabs.Content value="climate">
							<ClimateTab quadrant={quadrantModalStore.quadrant} />
						</Tabs.Content>

						<Tabs.Content value="location">
							<LocationTab quadrant={quadrantModalStore.quadrant} />
						</Tabs.Content>
					</div>
				</div>
			</Tabs.Root>
		</Dialog.Content>
	</Dialog.Root>
{/if}
