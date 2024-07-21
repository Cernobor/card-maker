<script lang="ts">
	import type { Tag } from "./types";
	import Card from "./Card.svelte"
	import { onMount } from "svelte";
	import { fetchTags } from "./fetchResource";

	export let card: Card;
	export let cardTypeProp = card.type;
	export let cardTypes;

	$: {card.type = cardTypeProp;
		if (cardTypeProp == 'Magický předmět') {
			card.in_set = false;
			card.set_name = 'Jméno setu (počet itemů v setu)';
		} else if (cardTypeProp == 'Volný aspekt') {
			card.in_set = false;
			card.set_name = 'Jméno rodiny aspektů';
		}
	}

	let tags: Tag[]|[] = [];
	onMount(async () => {
		tags = await fetchTags();
    });

	function handleTagsChange(e) {
        if (e.target.checked) {
            card.tags.push(e.target.value)
        } else {
            card.tags = card.tags.filter((_, i) => i !== card.tags.indexOf(e.target.value));
        }
		console.log(card.tags)
	}

</script>

<div class="inputs">
	<form class="card-input-form">
		<label for="name">Jméno:</label>

		<input type="text" placeholder="Name" id="name" bind:value={card.name} />
		<label for="type">Typ:</label>
		<select bind:value={cardTypeProp}>
			{#each cardTypes as type (type)}
				<option value={type}>{type}</option>
			{/each}
		</select>

		<label for="fluff">Fluff:</label>

		<textarea bind:value={card.fluff} placeholder="fluff" id="fluff" />
		<label for="efect">Efekt/pravidla:</label>
		<textarea bind:value={card.effect} placeholder="efekt" id="efect" />

		{#if card.type == 'Magický předmět'}
			<label for="nonremovable">Neodložitelný:</label>
			<input type="checkbox" class="checkbox" bind:checked={card.nonRemovable} id="nonremovable" />

			<label for="in_set">V setu:</label>
			<input type="checkbox" class="checkbox" bind:checked={card.in_set} id="in_set" />
			{#if card.in_set}
				<label for="set_name">Jméno setu:</label>
				<input type="text" bind:value={card.set_name} id="set_name" />
			{/if}
		{/if}

		{#if card.type == 'Volný aspekt'}
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
				<input type="checkbox" id={tag.name} class="checkbox" value={tag.name} on:change={handleTagsChange} />
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
