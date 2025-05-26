<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { quadrantModalStore } from '$lib/stores/quadrant-modal-store.svelte';
	import { Badge } from '../ui/badge';
	import { Leaf, Thermometer, MapPin } from '@lucide/svelte';
	import * as Tabs from '$lib/components/ui/tabs';
	import ClimateTab from './tabs/climate-tab.svelte';
	import TaxonomyTab from './tabs/taxonomy-tab.svelte';
	import LocationTab from './tabs/location-tab.svelte';
	import { cn } from '@/utils';

	let activeTab: 'taxonomy' | 'climate' | 'location' = $state('taxonomy');

	$effect(() => {
		if (quadrantModalStore.isOpen) {
			activeTab = 'taxonomy';
		}
	});
</script>

{#if quadrantModalStore.quadrant}
	<Dialog.Root bind:open={quadrantModalStore.isOpen}>
		<Dialog.Content class="overflow-clip p-0 sm:max-w-4xl">
			<Tabs.Root bind:value={activeTab}>
				<Dialog.Header class="bg-green-50 px-6 pt-6">
					<div class="flex w-full items-start justify-between">
						<div class="w-full">
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

					<div class="flex w-full justify-center sm:justify-start">
						<Tabs.List class="w-full bg-transparent shadow-none sm:w-fit">
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
					</div>
				</Dialog.Header>

				<div class="grid max-h-[calc(100lvh-157px)] gap-6 overflow-y-auto p-4 sm:p-6">
					<div
						class={cn(
							'w-full max-w-full md:col-span-2',
							activeTab === 'taxonomy' && 'md:col-span-2'
						)}
						data-tab={activeTab}
					>
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
