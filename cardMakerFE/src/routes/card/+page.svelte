<script lang="ts">
	import Card from '$lib/components/Card.svelte';
	import CardForm from '$lib/components/CardForm.svelte';
	import { api } from '$lib/stores/store';
	import type { CardCreate, CardType } from '$lib/interfaces';

	let cardComponent;
	let cardTypes: CardType[];
	let card: CardCreate;
	let currentUserId: number | null = null;

	async function load() {
		/***
		 * Get card types and initialize an empty card.
		 */
		cardTypes = await $api.getCardTypes();
		if (!cardTypes) {
			throw new Error('Cannot get card types!');
		}
		if ($api.currentUser) {
			currentUserId = $api.currentUser.id;
		}
		card = {
			name: 'Card Name',
			card_type_id: cardTypes[0].id,
			user_id: currentUserId,
			fluff: 'Card Fluff',
			effect: 'Efekt/pravidla karty',
			in_set: false,
			set_name: '',
			tags: [],
			size: null,
		};
	}
</script>

<div class="cardmaker-body">
	{#await load()}
		<h1>loading...</h1>
	{:then}
		<div>
			<CardForm bind:card bind:cardTypes />
		</div>
		<div class="card-view">
			{#if !$api.loggedIn}
				<p class="warning">
					Nejsi přihlášený. Pro uložení karty se přihlaš <a href="/login">zde</a>.
				</p>
			{/if}
			<Card bind:card bind:this={cardComponent} bind:cardTypes />
			<button on:click={cardComponent.downloadCard}>Uložit a stáhnout</button>
			<button on:click={cardComponent.sentCardToAPI} disabled={!$api.loggedIn}>Uložit</button>
		</div>
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
