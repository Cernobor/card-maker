<script lang="ts">
	import type { CardCreate, Tag } from '$lib/interfaces';
	import { onMount } from 'svelte';
	import ChangeTagDropdown from './ChangeTagDropdown.svelte';
	import TagLabels from './TagLabels.svelte';

	export let card: CardCreate;
	export let tags: Tag[];

	let newTag: string = '';
	let dropdownComponent: ChangeTagDropdown;
	let tagsContainTagName: Function;

	function handleAddNewTag(event: Event) {
		/**
		 * Add new tag to tag list and to card tags if it is not already there.
		 */
		event.preventDefault();
		if (newTag.trim() !== '' && !tagsContainTagName(newTag, card.tags)) {
			if (!tagsContainTagName(newTag, tags)) {
				tags = [...tags, { name: newTag.trim() }];
			}
			card.tags = [...card.tags, { name: newTag.trim() }];
		}
		newTag = '';
	}

	function handleKeydown(event: KeyboardEvent) {
		/**
		 * Allow user to confirm tag adding by pressing enter key.
		 */
		if (event.key === 'Enter') {
			event.preventDefault();
			handleAddNewTag(event);
		}
	}

	onMount(() => {
		tagsContainTagName = (newTag: string, activeTags: Tag[]): boolean => {
			return dropdownComponent.tagsContainTagName(newTag, activeTags);
		};
	});
</script>

<div class="tag-selector">
	<TagLabels bind:activeLabels={card.tags} />
	<ChangeTagDropdown
		bind:this={dropdownComponent}
		bind:activeTags={card.tags}
		bind:tags
		cssClass="add-tag"
	/>
	<div class="center">
		<input class="tag-input" type="text" bind:value={newTag} required on:keydown={handleKeydown} />
		<button class="add-tag" on:click={handleAddNewTag}>Nový tag</button>
	</div>
</div>
