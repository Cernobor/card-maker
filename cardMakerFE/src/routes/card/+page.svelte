<script lang="ts">
	import Card from '$lib/components/Card.svelte';
	import CardForm from '$lib/components/CardForm.svelte';
	import { fetchTags } from '$lib/fetchResource';
	import type { Tag } from '$lib/interfaces';
	import { onMount } from 'svelte';
	let cardTypes = ['Magický předmět', 'Volný aspekt', 'Lokace'];

	let card = {
		name: 'Card Name',
		type: cardTypes[0],
		fluff: 'Card Fluff',
		effect: 'Efekt/pravidla karty',
		nonRemovable: true,
		in_set: false,
		set_name: 'Jméno setu (počet itemů v setu)',

		tags: []
	};

	let cardComponent;

	let tags: Tag[] | [] = [];
	onMount(async () => {
		tags = await fetchTags();
	});

	function handleTagsChange() {}
</script>

<div class="cardmaker-body">
	<div class="inputs">
		<CardForm bind:card bind:cardTypes />
	</div>

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

	<div class="card-view">
		<Card bind:card bind:this={cardComponent} />
		<button on:click={cardComponent.saveCard}>Save</button>
	</div>
</div>

<style>
	.card-view {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 20px;
		color: black;
	}
</style>
