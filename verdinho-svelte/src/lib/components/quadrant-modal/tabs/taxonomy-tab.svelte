<script lang="ts">
	import { Separator } from '@/components/ui/separator';
	import type { QuadrantData } from '@/stores/mapStore.svelte';

	let props: {
		quadrant: QuadrantData;
	} = $props();

	const quadrant = $derived(props.quadrant);
</script>

<div class="space-y-4">
	<div class="grid grid-cols-2 gap-4">
		<div>
			<p class="text-muted-foreground text-sm font-medium">Classe</p>
			<p class="text-base">{quadrant.plantRecommendation.class}</p>
		</div>
		<div>
			<p class="text-muted-foreground text-sm font-medium">Família</p>
			<p class="text-base">
				{quadrant.plantRecommendation.family}
			</p>
		</div>
		<div>
			<p class="text-muted-foreground text-sm font-medium">Ordem</p>
			<p class="text-base">{quadrant.plantRecommendation.order}</p>
		</div>
		<div>
			<p class="text-muted-foreground text-sm font-medium">Gênero</p>
			<p class="text-base">
				{quadrant.plantRecommendation.gender}
			</p>
		</div>
	</div>

	<Separator />

	<div>
		<h4 class="text-muted-foreground mb-2 text-sm font-medium">Características</h4>
		<ul class="list-disc space-y-1 pl-5 text-sm">
			<li>Planta nativa da região</li>
			<li>Boa adaptação a solos arenosos</li>
			<li>Resistente a períodos de seca</li>
			<li>Atrai polinizadores locais</li>
		</ul>
	</div>
</div>
