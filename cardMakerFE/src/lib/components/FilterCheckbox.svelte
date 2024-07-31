<script lang="ts">
	import type { Tag } from '$lib/interfaces';
	export let options: Tag[];
	export let activeTags: Tag[];

	function handleChange(event: Event) {
		/**
		 * Update selected tags array according to checked checkboxes.
		 */
		const target = event.target as HTMLInputElement;
		if (target.checked) {
			activeTags = [...activeTags, { name: target.value }];
		} else {
			activeTags = activeTags.filter((_, i) => i !== activeTags.indexOf({ name: target.value }));
		}
	}
</script>

<div>
	<h3 class="filter-title">Tagy</h3>
	<div class="all-checkboxes-container">
		{#each options as option}
			<div class="checkbox-container">
				<label for={option.name}>{option.name}</label>
				<input
					type="checkbox"
					id={option.name}
					class="checkbox"
					value={option.name}
					on:change={handleChange}
				/>
			</div>
		{/each}
	</div>
</div>
