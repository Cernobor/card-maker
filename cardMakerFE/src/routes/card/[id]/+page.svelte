<script lang="ts">
	import { api } from '$lib/stores/store';
	/** @type {import('./$types').PageData} */
	import Card from '$lib/components/Card.svelte';
	import CardForm from '$lib/components/CardForm.svelte';
	import type { CardCreate, CardType, Mode } from '$lib/interfaces';
	import ErrorMessage from '$lib/components/ErrorMessage.svelte';

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


	import { openModal } from 'svelte-modals'
	import CardDeleteModal from '$lib/components/CardDeleteModal.svelte';

</script>

<div class="cardmaker-body">
	{#await loadCard()}
		<h1>loading...</h1>
	{:then}
		<div>
			<CardForm bind:card bind:cardTypes bind:mode />
		</div>
		<div class="card-view">
			{#if !$api.loggedIn}
				<p class="warning">
					Nejsi přihlášený. Pro uložení změn či smazání karty se přihlaš <a href="/login">zde</a>.
				</p>
			{/if}
			<Card
				bind:card
				bind:mode
				bind:this={cardComponent}
				bind:cardTypes
				bind:cardId={data.cardId}
			/>
			<button on:click={cardComponent.downloadCard}>Uložit změny a stáhnout</button>
			<button on:click={cardComponent.sentCardToAPI} disabled={!$api.loggedIn}>Uložit změny</button>
			<button  on:click={() => {openModal(CardDeleteModal, {cardName: card.name, cardId : data.cardId})}}>Smazat kartu</button>
		</div>
	{:catch}
		<ErrorMessage errorMessage="Karta s id {data.cardId} neexistuje" />
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
