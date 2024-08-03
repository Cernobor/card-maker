<script lang="ts">
	import type { CardCreate, Tag } from '$lib/interfaces';
	import { onMount } from 'svelte';
	import ChangeTagDropdown from './ChangeTagDropdown.svelte';
	import TagLabels from './TagLabels.svelte';

	export let card: CardCreate;
	export let tags: Tag[];

	let newTag: string = '';
	let dropdownComponent: ChangeTagDropdown;
	let checkIfContainsTagName: Function;

	onMount(() => {
		checkIfContainsTagName = (newTag: string, activeTags: Tag[]) => {
			return dropdownComponent.checkIfContainsTagName(newTag, activeTags);
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
		<input class="tag-input" type="text" bind:value={newTag} />
		<button
			class="add-tag"
			on:click={(event) => {
				if (newTag.trim() === '') {
					event.preventDefault();
				} else {
					if (checkIfContainsTagName(newTag, tags)) {
						event.preventDefault();
						alert('Tento tag už existuje.');
					} else {
						tags = [...tags, { name: newTag.trim() }];
						card.tags = [...card.tags, { name: newTag.trim() }];
					}
					newTag = '';
				}
			}}>Nový tag</button
		>
	</div>
</div>
