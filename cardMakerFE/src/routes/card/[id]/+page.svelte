<script>
	import { goto } from '$app/navigation';
	import { PUBLIC_BASE_API_URL } from '$env/static/public';
	/** @type {import('./$types').PageData} */
	export let data;

	import Card from '$lib/Card.svelte';
	import CardForm from '$lib/CardForm.svelte';

	let mode = 'update';
	let cardTypes = ['Volný aspekt', 'Lokace', 'Magický předmět'];
	let card = {};
	let loadProgress;
	let cardComponent;

	async function deleteCard() {
		try {
			const response = await fetch(PUBLIC_BASE_API_URL + '/cards/' + data.card_id, {method:"DELETE"});
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const result = await response.json();
			console.log(result);
			goto('/card/list');
		} catch (error) {
			console.log(error);
			console.error(error.message);
		}
	}

	async function getCard() {
		try {
			const response = await fetch('/cards/' + data.card_id);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const json = await response.json();

			return json;
		} catch (e) {
			console.error(e.message);
		}
	}

	async function loadCard() {
		const cardData = await getCard();
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
