<script>
	import { Github, Info, Loader2 } from '@lucide/svelte';
	import { buttonVariants } from './ui/button';
	import { Separator } from './ui/separator';
	import { mapState } from '@/stores/mapStore.svelte';
</script>

<div
	class="bg-background z-1000 fixed bottom-0 left-0 right-0 flex h-auto flex-col items-center justify-between px-4 py-2 sm:h-16 sm:flex-row sm:py-0"
>
	<div class="mb-2 flex items-center justify-between gap-2 sm:mb-0">
		{#if mapState.quadrants.length > 0}
			<div class="flex items-center gap-1 text-sm text-gray-600">
				<Info size={16} />
				<span>Clique na área verde ou dê duplo clique no nome da planta para mais informações</span>
			</div>
		{:else if mapState.isProcessing}
			<div class="flex items-center gap-1 text-sm text-gray-600">
				<Loader2 class="animate-spin" size={16} />
				<span>Processando quadrantes...</span>
			</div>
		{:else}
			<div class="flex items-center gap-1 text-sm text-gray-600">
				<Info size={16} />
				<span>
					Desenhe um retângulo no mapa para analisar área de reflorestamento usando a ferramenta de
					desenho no canto superior esquerdo.
				</span>
			</div>
		{/if}
	</div>

	<div class="flex h-5 items-center gap-2">
		<span>
			Feito com
			<a
				class="text-blue-500"
				href="https://leafletjs.com"
				target="_blank"
				rel="noopener noreferrer"
			>
				Leaflet
			</a>
		</span>

		<Separator orientation="vertical" />

		<a
			href="https://github.com/nicholascostadev/verdinho"
			target="_blank"
			rel="noopener noreferrer"
			class={buttonVariants({ variant: 'ghost' })}
		>
			Ver no GitHub
			<Github size={24} />
		</a>
	</div>
</div>
