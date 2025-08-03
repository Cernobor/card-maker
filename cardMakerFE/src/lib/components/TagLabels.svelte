<script lang="ts">
	import type { Tag } from '$lib/interfaces';
	import { createEventDispatcher } from 'svelte';

	export let activeLabels: Tag[];

	const dispatch = createEventDispatcher();

	function handleRemove(label: Tag) {
		dispatch('remove', label);
	}
</script>

<div class="labels">
	<ul class="labels">
		{#each activeLabels as label}
			<div class="tag-label">
				<li>
					{label.name}
					<button class="tag-label-button" on:click={() => handleRemove(label)}>✖️</button>
				</li>
			</div>
		{/each}
	</ul>
</div>
