<script lang="ts">
	import ArrowLeftIcon from '@lucide/svelte/icons/arrow-left';
	import type { WithoutChildren } from 'bits-ui';
	import { getEmblaContext } from './context.js';
	import { cn } from '$lib/utils.js';
	import { type Props } from '$lib/components/ui/button/index.js';

	let { class: className, ...restProps }: WithoutChildren<Props> = $props();

	const emblaCtx = getEmblaContext('<Carousel.Previous/>');
</script>

<button
	data-slot="carousel-previous"
	class={cn(
		'disabeld:cursor-not-allowed absolute flex size-8 items-center justify-center rounded-full bg-black/40 text-white backdrop-blur-sm disabled:opacity-50',
		emblaCtx.orientation === 'horizontal'
			? 'left-2 top-1/2 -translate-y-1/2'
			: '-top-12 left-1/2 -translate-x-1/2 rotate-90',
		className
	)}
	disabled={!emblaCtx.canScrollPrev}
	onclick={emblaCtx.scrollPrev}
	onkeydown={emblaCtx.handleKeyDown}
	{...restProps}
>
	<ArrowLeftIcon class="size-4" />
	<span class="sr-only">Previous slide</span>
</button>
