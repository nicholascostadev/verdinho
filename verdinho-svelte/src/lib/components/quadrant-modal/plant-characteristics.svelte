<script lang="ts">
	import { Info, Leaf } from '@lucide/svelte';
	import MarkdownRenderer from '../markdown-renderer.svelte';
	import * as Tooltip from '../ui/tooltip';
	import { Skeleton } from '../ui/skeleton';

	let response = $state('');
	let isFetching = $state(true);
	let shouldFetch = true;

	const {
		cientificName
	}: {
		cientificName: string;
	} = $props();

	$effect(() => {
		if (!shouldFetch || !cientificName) return;

		isFetching = true;
		fetch(`/api/describe?plant_name=${cientificName}`, {
			headers: { 'Content-Type': 'application/json' }
		}).then(async (res) => {
			await new Promise((resolve) => setTimeout(resolve, 1000));
			const reader = res.body?.getReader();
			if (!reader) {
				throw new Error('Response body is not a ReadableStream');
			}
			let accumulatedResponse = '';
			while (true) {
				const { done, value } = await reader.read();
				if (done) {
					response = response.slice(0, -3);
					break;
				}
				accumulatedResponse += new TextDecoder().decode(value);
				response = accumulatedResponse + '...';
				isFetching = false;
			}
		});
	});
</script>

<div class="space-y-3">
	<div class="flex items-center gap-2">
		<div class="rounded-full bg-green-100 p-2">
			<Leaf class="h-4 w-4 text-green-600" />
		</div>
		<h4 class="text-sm font-semibold text-gray-900">Características</h4>
		<Tooltip.Provider delayDuration={0}>
			<Tooltip.Root>
				<Tooltip.Trigger>
					<Info class="h-4 w-4" />
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>
						Esta descrição das características é gerada por inteligência artificial e pode conter
						imprecisões ou erros.
					</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</Tooltip.Provider>
	</div>

	{#if isFetching && !response}
		<div class="space-y-4 rounded-lg border border-gray-200 bg-gray-50 p-6 text-center">
			<Skeleton class="h-24 w-full" />
			<div>
				<Skeleton class="mt-8 h-6 w-36 max-w-full" />
			</div>
			<div class="space-y-2">
				<div class="flex items-center gap-4">
					<Skeleton class="h-4 w-4" />
					<Skeleton class="h-4 w-full" />
				</div>
				<div class="flex items-center gap-4">
					<Skeleton class="h-4 w-4" />
					<Skeleton class="h-4 w-full" />
				</div>
				<div class="flex items-center gap-4">
					<Skeleton class="h-4 w-4" />
					<Skeleton class="h-4 w-full" />
				</div>
			</div>
		</div>
	{:else if response}
		<div class="rounded-lg border border-gray-200 bg-gray-50 p-4">
			<MarkdownRenderer text={response} />
		</div>
	{:else}
		<div class="rounded-lg border border-gray-200 bg-gray-50 p-6 text-center">
			<div class="flex flex-col items-center gap-2">
				<div class="rounded-full bg-gray-200 p-3">
					<Leaf class="h-6 w-6 text-gray-400" />
				</div>
				<p class="text-sm text-gray-500">
					Informações detalhadas sobre características não disponíveis no momento
				</p>
			</div>
		</div>
	{/if}
</div>
