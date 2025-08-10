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
				card.size = null;
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

	function handleSizeChange(event: Event) {
		const input = event.currentTarget as HTMLInputElement;
		card.size = input.value;
	}
</script>

<div class="inputs">
	<form class="card-input-form {currentCardType.name === 'Lokace' ? 'grid-one' : 'grid-two'}">
		<div class="box">
			<div class="form-item">
				<label for="name">Jméno:</label>
				<input type="text" placeholder="název" id="name" bind:value={card.name} />
			</div>
			<div class="form-item">
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
			</div>
		</div>

		<div class="box">
			{#if currentCardType.name == 'Lokace' || currentCardType.name == 'Recept' || currentCardType.name == 'Zaříkadlo'}
				<div>
					<label for="sizes">Velikost karty:</label>
					<div class="sizes" id="sizes">
						<label>
							<input
								checked={card.size === 'small'}
								on:change={handleSizeChange}
								type="radio"
								name="amount"
								value="small"
							/> malá
						</label>
						{#if currentCardType.name == 'Lokace'}
						<label>
							<input
								checked={card.size === 'medium'}
								on:change={handleSizeChange}
								type="radio"
								name="amount"
								value="medium"
							/> střední
						</label>
						{/if}
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
				</div>
			{/if}

			{#if currentCardType.name == 'Magický předmět'}
				<div class="columns">
					<div class="form-item">
						<label for="in_set">V setu:</label>
						<Checkbox
							checked={card.in_set}
							onChange={(checked) => (card.in_set = checked)}
							id="in_set"
						/>
					</div>
					<div class={`form-item ${card.in_set ? '' : 'disabled-input'}`}>
						<!-- {#if card.in_set} -->
						<label for="set_name">Jméno setu:</label>
						<input type="text" bind:value={card.set_name} id="set_name" />
						<!-- {/if} -->
					</div>
				</div>
			{/if}

			{#if currentCardType.name == 'Volný aspekt'}
				<div class="columns">
					<div class="form-item">
						<label for="aspectFamily">V rodině apektů:</label>
						<Checkbox
							checked={card.in_set}
							onChange={(checked) => (card.in_set = checked)}
							id="aspectFamily"
						/>
					</div>
					<div class={`form-item ${card.in_set ? '' : 'disabled-input'}`}>
						<!-- {#if card.in_set} -->
						<label for="aspectFamilyName">Jméno rodiny aspektů:</label>
						<input type="text" bind:value={card.set_name} id="aspectFamilyName" />
						<!-- {/if} -->
					</div>
				</div>
			{/if}
			<TagsSelector bind:card bind:tags />
		</div>

		<div class="form-item box">
			<div class="form-item">
				<div class="tooltip">
					<label for="fluff">Fluff:</label>
					<div class="help-text">
						<HelpText />
					</div>
				</div>
				<textarea bind:value={card.fluff} placeholder="fluff" id="fluff" />
			</div>
		</div>

		<div class="form-item box">
			<div class="form-item">
				<div class="tooltip">
					<label for="efect">Efekt/pravidla:</label>
					<div class="help-text">
						<HelpText />
					</div>
				</div>
				<textarea bind:value={card.effect} placeholder="efekt/pravidla" id="efect" />
			</div>
		</div>
	</form>
</div>

<style>
	.card-input-form {
		display: grid;
		gap: 50px;
	}

	.card-input-form.grid-one {
		grid-template-columns: 1fr;
		gap: 20px;
	}

	.card-input-form.grid-two {
		grid-template-columns: repeat(2, 1fr);
		gap: 50px;
	}

	.box {
		background-color: #161a20;
		padding: 30px;
		border-radius: 15px;
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
		display: flex;
		flex-direction: column;
		gap: 25px;
		position: relative;
		overflow: hidden;
	}

	.inputs {
		width: 100%;
		max-width: 1000px;
		margin: 0 auto;
	}

	input {
		height: 30px;
	}

	select {
		height: 38px;
		box-sizing: border-box;
		padding: 0 5px;
	}

	.tooltip {
		max-width: 350px;
	}

	textarea {
		width: 100%;
		min-height: 150px;
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

	.columns {
		display: flex;
		flex-direction: row;
		gap: 15px;
		flex: 1;
		justify-content: space-between;
		align-items: center;
	}

	.columns .form-item {
		width: 50%;
	}

	.form-item {
		display: flex;
		flex-direction: column;
		flex: 1;
		margin: 0;
		gap: 7px;
	}

	.disabled-input {
		opacity: 0.5;
	}

	.disabled-input input {
		pointer-events: none;
	}
</style>
