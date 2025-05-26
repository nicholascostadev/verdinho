<script lang="ts">
	import ArrowRightIcon from '@lucide/svelte/icons/arrow-right';
	import type { WithoutChildren } from 'bits-ui';
	import { getEmblaContext } from './context.js';
	import { cn } from '$lib/utils.js';
	import { type Props } from '$lib/components/ui/button/index.js';

	let { class: className, ...restProps }: WithoutChildren<Props> = $props();

	const emblaCtx = getEmblaContext('<Carousel.Next/>');
</script>

<button
	data-slot="carousel-next"
	class={cn(
		'absolute flex size-8 items-center justify-center rounded-full bg-black/40 text-white backdrop-blur-sm disabled:cursor-not-allowed disabled:opacity-50',
		emblaCtx.orientation === 'horizontal'
			? 'right-2 top-1/2 -translate-y-1/2'
			: '-bottom-12 left-1/2 -translate-x-1/2 rotate-90',
		className
	)}
	disabled={!emblaCtx.canScrollNext}
	onclick={emblaCtx.scrollNext}
	onkeydown={emblaCtx.handleKeyDown}
	{...restProps}
>
	<ArrowRightIcon class="size-4" />
	<span class="sr-only">Next slide</span>
</button>
