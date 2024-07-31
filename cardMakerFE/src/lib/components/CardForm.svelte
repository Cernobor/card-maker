<script lang="ts">
	import type { Tag, CardType, CardCreate } from '$lib/interfaces';
	import { api } from '$lib/stores/store';
	import { onMount } from 'svelte';

	export let card: CardCreate;
	export let cardTypes: CardType[];

	let currentCardType: CardType = { id: 0, name: '' };

	let tags: Tag[] = [];
	onMount(async () => {
		try {
			tags = await $api.getTags();
			console.log(tags);
			cardTypes = await $api.getCardTypes();
			currentCardType = cardTypes[0];
		} catch {
			alert('nejde to');
		}
	});

	$: if (currentCardType) {
		console.log('card types are here...');
		card.card_type_id = currentCardType.id;
		if (currentCardType.name == 'Magický předmět') {
			card.in_set = false;
			card.set_name = 'Jméno setu (počet itemů v setu)';
		} else if (currentCardType.name == 'Volný aspekt') {
			card.in_set = false;
			card.set_name = 'Jméno rodiny aspektů';
		}
	}

	function handleTagsChange(event: Event) {
		const target = event.target as HTMLInputElement;
		if (target.checked) {
			card.tags.push({ name: target.value });
		} else {
			card.tags = card.tags.filter((_, i) => i !== card.tags.indexOf({ name: target.value }));
		}
		console.log(card.tags);
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
		<div class="checkbox-container">
			{#each tags as tag}
				<label for={tag.name}>{tag.name}</label>
				<input
					type="checkbox"
					id={tag.name}
					class="checkbox"
					value={tag.name}
					on:change={handleTagsChange}
				/>
			{/each}
		</div>
	</form>
</div>

<style>
	textarea {
		width: 400px;
		height: 100px;
	}
</style>
