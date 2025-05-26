<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { Expand } from '@lucide/svelte';
	import PlantGallery from './plant-gallery.svelte';

	const {
		cientificName
	}: {
		cientificName: string;
	} = $props();
</script>

<Dialog.Root>
	<Dialog.Trigger
		class="absolute bottom-4 right-4 flex items-center gap-1 rounded-full bg-black/40 p-2 backdrop-blur-sm"
	>
		<Expand class="h-4 w-4 text-white" />
	</Dialog.Trigger>
	<Dialog.Content class="sm:max-h-fit sm:max-w-[80lvh]">
		<PlantGallery {cientificName} isFullScreenViewing />
	</Dialog.Content>
</Dialog.Root>
