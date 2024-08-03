<script lang="ts">
	import type { Tag, CardType, CardCreate } from '$lib/interfaces';
	import { api } from '$lib/stores/store';
	import { onMount } from 'svelte';
	import TagsSelector from './TagsSelector.svelte';
	import type { Mode } from '$lib/interfaces';

	export let card: CardCreate;
	export let cardTypes: CardType[];
	export let mode: Mode = 'create';

	let currentCardType: CardType = { id: 0, name: '' };
	let tags: Tag[] = [];

	onMount(async () => {
		/**
		 * Get tags and card types.
		 */
		try {
			tags = await $api.getTags();
			tags = tags.filter((tag) => {
				return tag.description != 'year';
			});
			cardTypes = await $api.getCardTypes();
			currentCardType = cardTypes[0];
			if (mode == 'create') {
				card.tags.push({ name: 'Neodložitelný' });
			}
		} catch {
			alert('Problem s nacitanim tagu nebo typu karet.');
		}
	});

	$: if (currentCardType) {
		card.card_type_id = currentCardType.id;
	}
</script>

<div class="inputs">
	<form class="card-input-form">
		<label for="name">Jméno:</label>

		<input type="text" placeholder="Name" id="name" bind:value={card.name} />
		<label for="type">Typ:</label>
		<select bind:value={currentCardType}>
			{#each cardTypes as type (type)}
				<option value={type}>{type.name}</option>
			{/each}
		</select>

		<label for="fluff">Fluff:</label>

		<textarea bind:value={card.fluff} placeholder="fluff" id="fluff" />
		<label for="efect">Efekt/pravidla:</label>
		<textarea bind:value={card.effect} placeholder="efekt" id="efect" />

		{#if currentCardType.name == 'Magický předmět'}
			<label for="in_set">V setu:</label>
			<input type="checkbox" class="checkbox" bind:checked={card.in_set} id="in_set" />
			{#if card.in_set}
				<label for="set_name">Jméno setu:</label>
				<input type="text" bind:value={card.set_name} id="set_name" />
			{/if}
		{/if}

		{#if currentCardType.name == 'Volný aspekt'}
			<label for="aspectFamily">V rodině apektů:</label>
			<input type="checkbox" class="checkbox" bind:checked={card.in_set} id="aspectFamily" />
			{#if card.in_set}
				<label for="aspectFamilyName">Jméno rodiny aspektů:</label>
				<input type="text" bind:value={card.set_name} id="aspectFamilyName" />
			{/if}
		{/if}
		<TagsSelector bind:card bind:tags />
	</form>
</div>

<style>
	textarea {
		width: 400px;
		height: 100px;
	}
</style>
