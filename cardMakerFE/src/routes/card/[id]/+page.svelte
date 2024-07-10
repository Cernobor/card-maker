<script>
	import { goto } from '$app/navigation';
	import { PUBLIC_BASE_API_URL } from '$env/static/public';
	/** @type {import('./$types').PageData} */
	export let data;
	let mode = 'update';

	import Card from '$lib/Card.svelte';
	import CardForm from '$lib/CardForm.svelte';

	let cardTypes = ['Volný aspekt', 'Lokace','Magický předmět'];

	async function deleteCard() {
		try {
			const response = await fetch(PUBLIC_BASE_API_URL + '/cardmaker/cards/' + data.card_id, {method:"DELETE"});
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
			const response = await fetch(PUBLIC_BASE_API_URL + '/cardmaker/cards/' + data.card_id);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const json = await response.json();
			return json;
		} catch (error) {
			console.error(error.message);
		}
	}
	let card = {};

	async function loadCard() {
		const cardData = await getCard();
		card = { ...cardData };
		card.type = cardTypes[cardData.card_type_id - 1];
	}
	loadCard();
	let cardComponent;
</script>

<div class="cardmaker-body">
	<div class="inputs">
		<CardForm bind:card bind:cardTypes cardTypeProp={card.type} />
	</div>

	<div class="card-view">
		<Card bind:card bind:mode bind:this={cardComponent} />
		<button on:click={cardComponent.saveCard}>Save edit</button>
		<button on:click={deleteCard}>Delete card</button>
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
