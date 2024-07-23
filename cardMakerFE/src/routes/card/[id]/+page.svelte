
<script>
	import { goto } from '$app/navigation';
	import { PUBLIC_BASE_API_URL } from '$env/static/public';
	import { api } from '$lib/stores/store';
	/** @type {import('./$types').PageData} */
	export let data;

	import Card from '$lib/components/Card.svelte';
	import CardForm from '$lib/components/CardForm.svelte';

	let mode = 'update';
	let cardTypes = ['Volný aspekt', 'Lokace', 'Magický předmět'];
	let card = {};
	let cardComponent;

	async function deleteCard() {
		try {
			const response = await fetch(PUBLIC_BASE_API_URL + '/cards/' + data.card_id, {
				method: 'DELETE'
			});
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			if (response.ok) {
				goto('/card/list');
			} else {
				throw new Error('Failed to delete card');
			}
		} catch (error) {
			console.log(error);
			console.error(error.message);
		}
	}

	async function getCard() {
		try {
			const response = await fetch(PUBLIC_BASE_API_URL + '/cards/' + data.card_id);
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
		console.log("kkkkk");
		const cardData = await getCard();
		card = { ...cardData };
		
		card.type = cardTypes[cardData.card_type_id - 1];
	}
	console.log("there")
	let loadProgress = api.getCard(data.card_id)
	console.log("here")

</script>

<div class="cardmaker-body">
	{#await  api.getCard(data.card_id)}
		<h1>loading...</h1>
	{:then}
	<div class="card-view"></div>
	lllll
	<!--
		<div class="inputs">
			{@debug loadProgress}
			<CardForm bind:card bind:cardTypes cardTypeProp={card.type} />
		</div>
		
		
		
			<Card bind:card bind:mode bind:this={cardComponent} />
			<button on:click={cardComponent.saveCard}>Save edit</button>
			<button on:click={deleteCard}>Delete card</button>
		</div>
		-->
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

