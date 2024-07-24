<script>
	import { api } from '$lib/stores/store';
	/** @type {import('./$types').PageData} */
	export let data;

	import Card from '$lib/components/Card.svelte';
	import CardForm from '$lib/components/CardForm.svelte';

	let mode = 'update';
	let cardTypes = ['Volný aspekt', 'Lokace', 'Magický předmět'];

	let card = {};
	let cardComponent;
</script>

<div class="cardmaker-body">
	{#await $api.getCard(data.card_id)}
		<h1>loading...</h1>
	{:then card_data}
		<div class="card-view">
			{(card = { ...card_data, type: cardTypes[card_data.card_type_id - 1] })}

			<div class="inputs">
				<CardForm bind:card bind:cardTypes cardTypeProp={card.type} />
			</div>

			<Card bind:card bind:mode bind:this={cardComponent} />
			<button on:click={cardComponent.saveCard}>Save edit</button>
			<button on:click={$api.deleteCard(card.id, '/card/list')}>Delete card</button>
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
