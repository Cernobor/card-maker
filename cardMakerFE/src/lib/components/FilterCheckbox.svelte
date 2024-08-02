<script lang="ts">
	/**
	 * @todo refactor this component and TagSelector into one component
	 */
	import type { Tag } from '$lib/interfaces';
	export let options: Tag[];
	export let activeTags: Tag[];

	function handleAddTag(event: Event) {
		/**
		 * Add tag to card tags if card does not contain it.
		 */
		const target = event.target as HTMLSelectElement;
		if (target.value) {
			if (!checkIfCardContainsTag(target.value)) {
				activeTags = [...activeTags, { name: target.value }];
			}
			target.value = '';
		}
	}

	function checkIfCardContainsTag(tag: string) {
		/**
		 * Compare given tag with card tags
		 * and return true if card has tags else false
		 */
		for (const cardTag of activeTags) {
			if (cardTag.name === tag) {
				return true;
			}
		}
		return false;
	}
</script>

<div>
	<h3 class="filter-title">Tagy</h3>
	<div class="labels">
		<ul class="labels">
			{#each activeTags as tag}
				<div class="tag-label">
					<li>
						{tag.name}
						<button
							class="tag-label-button"
							on:click={() => {
								activeTags = activeTags.filter((cardTag) => {
									return cardTag.name !== tag.name;
								});
							}}>X</button
						>
					</li>
				</div>
			{/each}
		</ul>
		<select class="add-tag" on:change={handleAddTag}>
			<option value=""></option>
			{#each options as tag}
				<option value={tag.name}>{tag.name}</option>
			{/each}
		</select>
	</div>
</div>
