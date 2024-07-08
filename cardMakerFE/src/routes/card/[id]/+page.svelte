<script>
	import { getCard } from '$lib/api';
	/** @type {import('./$types').PageData} */
	export let data;

	import Card from '$lib/Card.svelte';
	import CardForm from '$lib/CardForm.svelte';

	let mode = 'update';
	let cardTypes = ['Volný aspekt', 'Lokace', 'Magický předmět'];
	let card = {};
	let loadProgress;
	let cardComponent;

	async function loadCard() {
		const cardData = await getCard(data.card_id);
		card = { ...cardData };
		card.type = cardTypes[cardData.card_type_id - 1];
	}

	loadProgress = loadCard();
</script>

<div class="cardmaker-body">
	{#await loadProgress}
		<h1>loading...</h1>
	{:then}
		<div class="inputs">
			<CardForm bind:card bind:cardTypes cardTypeProp={card.type} />
		</div>

		<div class="card-view">
			<Card bind:card bind:mode bind:this={cardComponent} />
			<button on:click={cardComponent.saveCard}>Save</button>
		</div>
	{:catch error}
		<h1>Karta s id {data.card_id} neexistuje</h1>
	{/await}
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
