<script lang="ts">
	import { getEmblaContext } from './context.js';

	const emblaCtx = getEmblaContext('<Carousel.Content/>');

	// Configuration for smart indicators
	const MAX_VISIBLE_DOTS = 7; // Maximum number of dots to show
	const SIDE_DOTS = Math.floor((MAX_VISIBLE_DOTS - 1) / 2); // Dots on each side of current

	// Calculate which dots to show
	const visibleDots = $derived.by(() => {
		const totalSnaps = emblaCtx.scrollSnaps.length;
		const currentIndex = emblaCtx.selectedIndex;

		if (totalSnaps <= MAX_VISIBLE_DOTS) {
			// Show all dots if we have few items
			return emblaCtx.scrollSnaps.map((_, index) => ({
				index,
				type: 'dot' as const,
				isActive: index === currentIndex
			}));
		}

		const dots: Array<{
			index: number;
			type: 'dot' | 'ellipsis';
			isActive: boolean;
		}> = [];

		// Always show first dot
		if (currentIndex > SIDE_DOTS + 1) {
			dots.push({ index: 0, type: 'dot', isActive: false });
			if (currentIndex > SIDE_DOTS + 2) {
				dots.push({ index: -1, type: 'ellipsis', isActive: false });
			}
		}

		// Show dots around current position
		const start = Math.max(0, Math.min(currentIndex - SIDE_DOTS, totalSnaps - MAX_VISIBLE_DOTS));
		const end = Math.min(totalSnaps - 1, Math.max(currentIndex + SIDE_DOTS, MAX_VISIBLE_DOTS - 1));

		for (let i = start; i <= end; i++) {
			if (i >= 0 && i < totalSnaps) {
				dots.push({ index: i, type: 'dot', isActive: i === currentIndex });
			}
		}

		// Always show last dot
		if (currentIndex < totalSnaps - SIDE_DOTS - 2) {
			if (currentIndex < totalSnaps - SIDE_DOTS - 3) {
				dots.push({ index: -2, type: 'ellipsis', isActive: false });
			}
			dots.push({ index: totalSnaps - 1, type: 'dot', isActive: false });
		}

		// Remove duplicates
		const uniqueDots = dots.filter(
			(dot, index, arr) =>
				dot.type === 'ellipsis' ||
				arr.findIndex((d) => d.index === dot.index && d.type === 'dot') === index
		);

		return uniqueDots;
	});
</script>

<div class="absolute bottom-4 left-1/2 -translate-x-1/2">
	<div class="flex items-center gap-1 rounded-full bg-black/40 px-3 py-2 backdrop-blur-sm">
		{#each visibleDots as item (item.type === 'ellipsis' ? `ellipsis-${item.index}` : item.index)}
			{#if item.type === 'ellipsis'}
				<div class="flex items-center justify-center px-1">
					<div class="flex gap-0.5">
						<div class="size-1 rounded-full bg-white/40"></div>
						<div class="size-1 rounded-full bg-white/40"></div>
						<div class="size-1 rounded-full bg-white/40"></div>
					</div>
				</div>
			{:else}
				<button
					class="size-2.5 rounded-full transition-all duration-200 hover:scale-110 focus:outline-none focus:ring-2 focus:ring-white/50 focus:ring-offset-2 focus:ring-offset-black/20 {item.isActive
						? 'scale-125 bg-white'
						: 'bg-white/40'}"
					onclick={() => emblaCtx.scrollTo(item.index)}
					aria-label="Go to slide {item.index + 1}"
				>
					<span class="sr-only">{item.index + 1}</span>
				</button>
			{/if}
		{/each}
	</div>

	<!-- Optional: Show current position text for many items -->
	{#if emblaCtx.scrollSnaps.length > 20}
		<div class="mt-2 text-center">
			<span
				class="rounded-full bg-black/60 px-2 py-1 text-xs font-medium text-white/70 backdrop-blur-sm"
			>
				{emblaCtx.selectedIndex + 1} / {emblaCtx.scrollSnaps.length}
			</span>
		</div>
	{/if}
</div>
