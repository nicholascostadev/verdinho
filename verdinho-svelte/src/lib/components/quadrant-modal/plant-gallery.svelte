<script lang="ts">
	import { ExternalLink, Info, Loader2 } from '@lucide/svelte';
	import { getPlantGallery } from '../../../services/http/get-plant-gallery';
	import * as Carousel from '../ui/carousel';
	import * as Tooltip from '../ui/tooltip';
	import { buttonVariants } from '../ui/button';
	import PlantGalleryFullscreenViewer from './plant-gallery-fullscreen-viewer.svelte';
	import { cn } from '@/utils';

	const {
		cientificName,
		isFullScreenViewing = false
	}: {
		cientificName: string;
		isFullScreenViewing?: boolean;
	} = $props();
</script>

<div class="flex max-h-full max-w-full flex-col items-center justify-start md:col-span-1">
	{#await getPlantGallery(cientificName)}
		<div
			class="relative aspect-square w-full overflow-hidden rounded-lg border border-green-100 bg-green-50"
		>
			<div class="flex h-full w-full items-center justify-center">
				<Loader2 class="h-4 w-4 animate-spin" />
			</div>
		</div>
	{:then data}
		<Carousel.Root
			class="relative aspect-square w-full overflow-hidden rounded-lg border border-green-100 bg-green-50"
		>
			<Carousel.Content>
				{#each data as item (item.identifier)}
					<Carousel.Item class={cn(isFullScreenViewing && 'h-full')}>
						<div class={cn('relative h-auto w-full', isFullScreenViewing && 'h-full')}>
							<img
								class={cn('h-auto w-full object-cover', isFullScreenViewing && 'object-contain')}
								src={item.identifier}
								alt={cientificName}
							/>
						</div>
					</Carousel.Item>
				{/each}
			</Carousel.Content>
			<Tooltip.Provider delayDuration={0}>
				<Tooltip.Root>
					<Tooltip.Trigger
						class="absolute right-4 top-4 rounded-full bg-black/40 p-1 text-white backdrop-blur-sm"
					>
						<Info class="h-4 w-4" />
					</Tooltip.Trigger>
					<Tooltip.Content>
						<p>A imagem é buscada dinamicamente do GBIF (https://www.gbif.org).</p>
					</Tooltip.Content>
				</Tooltip.Root>
			</Tooltip.Provider>
			<Carousel.Indicator />
			{#if !isFullScreenViewing}
				<PlantGalleryFullscreenViewer {cientificName} />
			{/if}
			<Carousel.Next />
			<Carousel.Previous />
		</Carousel.Root>
	{/await}
	{#if !isFullScreenViewing}
		<a
			href={`https://www.google.com/search?q=${cientificName}`}
			target="_blank"
			rel="noopener noreferrer"
			class={buttonVariants({
				variant: 'outline',
				class: 'mt-4 w-full'
			})}
		>
			Ver detalhes completos <ExternalLink class="h-4 w-4" />
		</a>
	{/if}
</div>
