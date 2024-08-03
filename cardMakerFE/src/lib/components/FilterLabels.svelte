<script lang="ts">
	import type { Tag } from '$lib/interfaces';
	import TagLabels from './TagLabels.svelte';
	import ChangeTagDropdown from './ChangeTagDropdown.svelte';

	export let options: Tag[];
	export let activeTags: Tag[];
</script>

<div>
	<h3 class="filter-title">Tagy</h3>
	<ChangeTagDropdown bind:tags={options} bind:activeTags cssClass="filter-tags" />
	<TagLabels bind:activeLabels={activeTags} />
</div>
