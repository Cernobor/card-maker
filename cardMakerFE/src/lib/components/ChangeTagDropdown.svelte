<script lang="ts">
	import type { Tag } from '$lib/interfaces';

	export let activeTags: Tag[];
	export let tags: Tag[];

	$: tags = tags.sort((tag1: Tag, tag2: Tag): number => {
		/**
		 * Sort tags alfabetically according to name.
		 */
		if (tag1.name < tag2.name) {
			return -1;
		}
		if (tag1.name > tag2.name) {
			return 1;
		}
		return 0;
	});

	function handleAddTag(event: Event): void {
		/**
		 * Add tag to card tags if card does not contain it.
		 */
		const target = event.target as HTMLSelectElement;
		if (target.value) {
			if (!tagsContainTagName(target.value, activeTags)) {
				activeTags = [...activeTags, { name: target.value }];
			}
			target.value = '';
		}
	}

	export function tagsContainTagName(tagName: string, activeTags: Tag[]): boolean {
		/**
		 * Compare given tag with card tags
		 * and return true if card has tags else false
		 */
		for (const activeTag of activeTags) {
			if (activeTag.name === tagName) {
				return true;
			}
		}
		return false;
	}
</script>

<div>
	<label for="tag-dropdown">Tagy</label>
	<select id="tag-dropdown" on:change={handleAddTag}>
		<option value="">Tagy</option>
		{#each tags as tag}
			<option value={tag.name}>{tag.name}</option>
		{/each}
	</select>
</div>
