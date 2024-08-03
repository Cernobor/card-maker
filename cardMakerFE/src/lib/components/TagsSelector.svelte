<script lang="ts">
	import type { CardCreate, Tag } from '$lib/interfaces';

	export let card: CardCreate;
	export let tags: Tag[];

	let newTag: string = '';

	function handleAddTag(event: Event):void {
		/**
		 * Add tag to card tags if card does not contain it.
		 */
		const target = event.target as HTMLSelectElement;
		if (target.value) {
			if (!checkIfCardContainsTag(target.value)) {
				card.tags = [...card.tags, { name: target.value }];
			}
			target.value = '';
		}
	}

	function checkIfCardContainsTag(tag: string):boolean {
		/**
		 * Compare given tag with card tags
		 * and return true if card has tags else false
		 */
		for (const cardTag of card.tags) {
			if (cardTag.name === tag) {
				return true;
			}
		}
		return false;
	}
</script>

<div class="tag-selector">
	<ul class="labels">
		{#each card.tags as tag}
			<div class="tag-label">
				<li>
					{tag.name}
					<button
						class="tag-label-button"
						on:click={() => {
							card.tags = card.tags.filter((cardTag) => {
								return cardTag.name !== tag.name;
							});
						}}>X</button
					>
				</li>
			</div>
		{/each}
	</ul>
	<div class="center">
		<select class="add-tag" on:change={handleAddTag}>
			<option value="">Tagy</option>
			{#each tags as tag}
				<option value={tag.name}>{tag.name}</option>
			{/each}
		</select>
	</div>
	<div class="center">
		<input class="tag-input" type="text" bind:value={newTag} />
		<button
			class="add-tag"
			on:click={(event) => {
				if (newTag.trim() === '') {
					event.preventDefault();
				} else {
					tags = [...tags, { name: newTag.trim() }];
					card.tags = [...card.tags, { name: newTag.trim() }];
					newTag = '';
				}
			}}>Nový tag</button
		>
	</div>
</div>
