<script lang="ts">
	import type { Tag, CardType, CardCreate } from '$lib/interfaces';
	import { api } from '$lib/stores/store';
	import { onMount } from 'svelte';
	import TagsSelector from './TagsSelector.svelte';
	import HelpText from './HelpText.svelte';
	import type { Mode } from '$lib/interfaces';
	import Checkbox from './Checkbox.svelte';

	export let card: CardCreate;
	export let cardTypes: CardType[];
	export let mode: Mode = 'create';

	let currentCardType: CardType = { id: 0, name: '' };
	let tags: Tag[] = [];

	function handleCardTypeChange() {
		/**
		 * Set card type ID to selected card type
		 * and reinitialize set parameters.
		 */
		card.card_type_id = currentCardType.id;
		card.in_set = false;
		card.set_name = '';
		if (mode == 'create') {
			if (currentCardType.name == 'Magický předmět') {
				card.tags = [...card.tags, { name: 'Neodložitelný' }];
			} else {
				card.tags = card.tags.filter((tag) => {
					return tag.name !== 'Neodložitelný';
				});
			}
			if (currentCardType.name == 'Lokace') {
				card.size = 'medium';
			} else {
				card.size = undefined;
			}
		}
	}

	onMount(async () => {
		/**
		 * Get tags and card types.
		 */
		try {
			tags = await $api.getTags();
			tags = tags.filter((tag) => {
				return tag.description != 'year';
			});
			cardTypes = await $api.getCardTypes();
			if (mode === 'update') {
				currentCardType = cardTypes.find((cardType) => {
					return cardType.id === card.card_type_id;
				})!;
			} else {
				currentCardType = cardTypes[0];
			}
		} catch {
			alert('Problem s nacitanim tagu nebo typu karet.');
		}
	});

	function handleSizeChange(event) {
		card.size = event.target.value;
	}
</script>

<div class="inputs">
	<form class="card-input-form">
		<label for="name">Jméno:</label>

		<input type="text" placeholder="Name" id="name" bind:value={card.name} />
		<label for="type">Typ:</label>
		<select
			bind:value={currentCardType}
			on:change={handleCardTypeChange}
			disabled={mode === 'update'}
		>
			{#each cardTypes as type (type)}
				<option value={type}>{type.name}</option>
			{/each}
		</select>

		{#if currentCardType.name == 'Lokace'}
			<label>Velikost karty:</label>

			<div class="sizes">
				<label>
					<input
						checked={card.size === 'small'}
						on:change={handleSizeChange}
						type="radio"
						name="amount"
						value="small"
					/> malá
				</label>
				<label>
					<input
						checked={card.size === 'medium'}
						on:change={handleSizeChange}
						type="radio"
						name="amount"
						value="medium"
					/> střední
				</label>
				<label>
					<input
						checked={card.size === 'large'}
						on:change={handleSizeChange}
						type="radio"
						name="amount"
						value="large"
					/> velká
				</label>
			</div>
		{/if}

		<div class="tooltip">
			<label for="fluff">Fluff:</label>
			<div class="help-text">
				<HelpText />
			</div>
		</div>
		<textarea bind:value={card.fluff} placeholder="fluff" id="fluff" />

		<div class="tooltip">
			<label for="efect">Efekt/pravidla:</label>
			<div class="help-text">
				<HelpText />
			</div>
		</div>

		<textarea bind:value={card.effect} placeholder="efekt" id="efect" />

		{#if currentCardType.name == 'Magický předmět'}
			<label for="in_set">V setu:</label>
			<Checkbox checked={card.in_set} onChange={(checked) => card.in_set = checked} id="in_set" />
			{#if card.in_set}
				<label for="set_name">Jméno setu:</label>
				<input type="text" bind:value={card.set_name} id="set_name" />
			{/if}
		{/if}

		{#if currentCardType.name == 'Volný aspekt'}
			<label for="aspectFamily">V rodině apektů:</label>
			<Checkbox checked={card.in_set} onChange={(checked) => card.in_set = checked} id="aspectFamily" />
			{#if card.in_set}
				<label for="aspectFamilyName">Jméno rodiny aspektů:</label>
				<input type="text" bind:value={card.set_name} id="aspectFamilyName" />
			{/if}
		{/if}
		<TagsSelector bind:card bind:tags />
	</form>
</div>

<style>
	textarea {
		width: 400px;
		height: 100px;
	}
	.tooltip .help-text {
		visibility: hidden;
		width: 280px;
		background-color: black;
		color: #fff;
		text-align: center;
		border-radius: 6px;
		padding: 5px 0;

		/* Position the tooltip */
		position: absolute;
		z-index: 1;
	}
	.tooltip:hover .help-text {
		visibility: visible;
	}
</style>
