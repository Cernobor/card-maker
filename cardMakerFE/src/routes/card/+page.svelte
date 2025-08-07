<script lang="ts">
	import { fade } from 'svelte/transition';
	import Card from '$lib/components/Card.svelte';
	import CardForm from '$lib/components/CardForm.svelte';
	import { api } from '$lib/stores/store';
	import {
		type CardCreate,
		type CardType,
		type ColorType,
		type FlashMessage,
		Color
	} from '$lib/interfaces';
	import DropdownButton from '$lib/components/DropdownButton.svelte';
	import PopUpMessage from '$lib/components/PopUpMessage.svelte';

	let cardComponent: Card;
	let cardTypes: CardType[];
	let card: CardCreate;
	let currentUserId: number | null = null;

	let flashMessages: FlashMessage[] = [];

	$: flashMessages;

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
			name: 'Název karty',
			card_type_id: cardTypes[0].id,
			user_id: currentUserId,
			fluff: 'Fluff text',
			effect: 'Efekt/pravidla karty',
			in_set: false,
			set_name: '',
			tags: [],
			size: null
		};
	}
</script>

<div class="content">
	<div class="flash-message-wrapper">
		{#each flashMessages as message (message.id)}
			<div class="pop-up-wrapper" in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
				<PopUpMessage
					{message}
					on:close={() => {
						flashMessages = flashMessages.filter((m) => m !== message);
					}}
				/>
			</div>
		{/each}
	</div>
	<h2 class="page-name">📄 Nová karta</h2>
	<div class="cardmaker-body-wrapper">
		<div class="cardmaker-body">
			{#await load()}
				<h1>loading...</h1>
			{:then}
				<div class="card-form-container">
					<CardForm bind:card bind:cardTypes />
				</div>
				<div class="card-view">
					{#if !$api.loggedIn}
						<p class="warning">
							Nejsi přihlášený. Pro uložení karty se přihlaš <a href="/login">zde</a>.
						</p>
					{/if}
					<Card
						bind:card
						bind:this={cardComponent}
						bind:cardTypes
						on:flash={(e) => {
							// e.detail is { message, color, id }
							flashMessages = [...flashMessages, e.detail];
						}}
					/>
					{#if cardComponent}
						<DropdownButton onSave={(...args) => cardComponent.save(...args)} />
					{/if}
				</div>
			{/await}
		</div>
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

	.pop-up-wrapper {
		justify-content: center;
		display: flex;
		margin-top: 15px;
	}
</style>
