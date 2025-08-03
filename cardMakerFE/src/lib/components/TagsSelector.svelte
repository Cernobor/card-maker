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
	let activeLabels: Tag[] = [];

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
		activeLabels = card.tags;
		tagsContainTagName = (newTag: string, activeTags: Tag[]): boolean => {
			return dropdownComponent.tagsContainTagName(newTag, activeTags);
		};
	});

	$: if (card.tags) {
		activeLabels = card.tags;
	}

	function handleRemoveTag(event: CustomEvent<Tag>) {
		const labelToRemove = event.detail;
		activeLabels = activeLabels.filter((label) => label.name !== labelToRemove.name);
		card.tags = activeLabels; // Keep card.tags in sync if needed
	}
</script>

<div class="tag-selector columns">
	<div class="form-item">
		<ChangeTagDropdown
			bind:this={dropdownComponent}
			bind:activeTags={card.tags}
			bind:tags
			inDetailTab={true}
		/>
	</div>
	<div class="form-item">
		<label for="">Nový tag</label>
		<input
			on:change={handleAddNewTag}
			type="text"
			bind:value={newTag}
			required
			on:keydown={handleKeydown}
		/>
	</div>
</div>
<div class="tag-selector">
	<TagLabels bind:activeLabels on:remove={handleRemoveTag} />
</div>

<style>
	input {
		height: 30px;
		border-radius: 6px;
	}

	.tag-selector {
		display: flex;
		flex-direction: row;
		margin: 0;
		padding: 0;
		max-width: 100%;
	}

	.columns {
		display: flex;
		flex-direction: row;
		gap: 15px;
		flex: 1;
		justify-content: space-between;
		align-items: center;
	}

	.columns .form-item {
		width: 50%;
	}

	.form-item {
		display: flex;
		flex-direction: column;
		flex: 1;
		margin: 0;
		gap: 7px;
	}
</style>
