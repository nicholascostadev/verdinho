<script lang="ts">
	import DOMPurify from 'dompurify';
	import { marked } from 'marked';

	const {
		text
	}: {
		text: string;
	} = $props();

	let parsed = $state('');

	$effect(() => {
		async function getParsedData() {
			const parsedd = await marked.parse(text);
			parsed = parsedd;
		}

		getParsedData();
	});
</script>

<div class="markdown-output prose">
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html DOMPurify.sanitize(parsed)}
</div>
