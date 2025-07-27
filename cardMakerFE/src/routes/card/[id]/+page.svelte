<script lang="ts">
	import { openModal } from 'svelte-modals';
	import { fade } from 'svelte/transition';
	import CardDeleteModal from '$lib/components/CardDeleteModal.svelte';
	import { api } from '$lib/stores/store';
	/** @type {import('./$types').PageData} */
	import Card from '$lib/components/Card.svelte';
	import CardForm from '$lib/components/CardForm.svelte';
	import {
		Color,
		type CardCreate,
		type CardType,
		type ColorType,
		type Mode
	} from '$lib/interfaces';
	import ErrorMessage from '$lib/components/ErrorMessage.svelte';
	import DropdownButton from '$lib/components/DropdownButton.svelte';
	import PopUpMessage from '$lib/components/PopUpMessage.svelte';

	export let data: { cardId: number };

	let mode: Mode = 'update';
	let cardTypes: CardType[];
	let card: CardCreate;
	let cardComponent: Card;

	let popUpDisplayed: boolean = false;
	let popUpMessage: string = '';
	let popUpColor: ColorType = Color.green;

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
	{#if popUpDisplayed}
		<div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
			<PopUpMessage
				message={popUpMessage}
				color={popUpColor}
				bind:isDisplayed={popUpDisplayed}
			/>
		</div>
	{/if}
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
				bind:message={popUpMessage}
				bind:messageColor={popUpColor}
				bind:popUpDisplayed={popUpDisplayed}
			/>
			{#if cardComponent}
				<DropdownButton onSave={(...args) => cardComponent.save(...args)} />
			{/if}
			<button
				on:click={() => {
					openModal(CardDeleteModal, { cardName: card.name, cardId: data.cardId });
				}}>Smazat kartu</button
			>
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

	.page-buttons {

	}
</style>
