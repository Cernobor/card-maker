<script lang="ts">
	import { api } from '$lib/stores/store';
	/** @type {import('./$types').PageData} */
	import Card from '$lib/components/Card.svelte';
	import CardForm from '$lib/components/CardForm.svelte';
	import type { CardCreate, CardType, Mode } from '$lib/interfaces';

	export let data: { cardId: number };

	let mode: Mode = 'update';
	let cardTypes: CardType[];
	let card: CardCreate;
	let cardComponent;

	async function loadCard() {
		/**
		 * Load and initialize card from database.
		 */
		const cardData = await $api.getCard(data.cardId);
		cardTypes = await $api.getCardTypes();
		if (!cardData) {
			throw new Error('Card does not exist');
		}
		card = { ...cardData };
	}
</script>

<div class="cardmaker-body">
	{#await loadCard()}
		<h1>loading...</h1>
	{:then}
		<div class="inputs">
			<CardForm bind:card bind:cardTypes />
		</div>
		<div class="card-view">
			{#if !$api.loggedIn}
				<p class="warning">
					Nejsi prihlaseny. Pro ulozeni ci smazani karty, se prihlas <a href="/login">zde</a>.
				</p>
			{/if}
			<Card bind:card bind:mode bind:this={cardComponent} bind:cardTypes />
			<button on:click={cardComponent.downloadCard}>Stahnout</button>
			<button on:click={cardComponent.sentCardToAPI} disabled={!$api.loggedIn}>Ulozit zmeny</button>
			<button on:click={() => $api.deleteCard(data.cardId, '/card/list')} disabled={!$api.loggedIn}
				>Smazat kartu</button
			>
		</div>
	{:catch}
		<h1>Karta s id {data.cardId} neexistuje</h1>
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
