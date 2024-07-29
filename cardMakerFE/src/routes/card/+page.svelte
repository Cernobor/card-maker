<script lang="ts">
	import Card from '$lib/components/Card.svelte';
	import CardForm from '$lib/components/CardForm.svelte';
	import { api } from '$lib/stores/store';
	import { onMount } from 'svelte';
	import type { CardCreate, Tag, CardType } from '$lib/interfaces';

	let cardComponent;
	let tags: Tag[] = [];
	let cardTypes: CardType[] = [];
	onMount(async () => {
		tags = await $api.getTags();
		cardTypes = await $api.getCardTypes();
	});

	let currentTags: Tag[] = [
		{
			name: 'Neodložitelný'
		}
	];
	let card: CardCreate = {
		name: 'Card Name',
		card_type_id: cardTypes[0].id,
		user_id: 1,
		fluff: 'Card Fluff',
		effect: 'Efekt/pravidla karty',
		in_set: false,
		set_name: 'Jméno setu (počet itemů v setu)',

		tags: currentTags
	};

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
		<Card bind:card bind:this={cardComponent} bind:cardTypes />
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
