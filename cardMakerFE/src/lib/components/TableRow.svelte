<script lang="ts">
	import type { UserPublic, CardType, CardGet } from '$lib/interfaces';
	import Checkbox from './Checkbox.svelte';

	export let card: CardGet;
	export let users: UserPublic[];
	export let types: CardType[];
	export let selectedCards: CardGet[];
	export let selectedCopies: Record<number, number>;

	let cardAuthor: string = 'waiting...';
	let cardType: string = 'waiting...';

	async function getUserNameByID(id: number) {
		return users.filter((user) => user.id == id)[0];
	}

	async function getTypeNameByID(id: number) {
		return types.filter((type) => type.id == id)[0];
	}

	$: if (users.length) {
		(async () => {
			const response = await getUserNameByID(card.user_id || 0);
			cardAuthor = response.username;
		})();
	}
	$: if (types.length) {
		(async () => {
			const response = await getTypeNameByID(card.card_type_id);
			cardType = response.name;
		})();
	}

	let selected = false;

	function handleCheckboxChange(checked: boolean) {
		if (checked) {
			if (!selectedCards.some((c) => c.id == card.id)) {
				selectedCards = [...selectedCards, card];
				selected = true;
				selectedCopies[card.id] = 1;
			}
		} else {
			selectedCards = selectedCards.filter((c) => c.id != card.id);
			selected = false;
			selectedCopies[card.id] = 1;
		}
	}

	function updateCheckbox(selectedCards: CardGet[]) {
		if (
			(selected && !selectedCards.includes(card)) ||
			(!selected && selectedCards.includes(card))
		) {
			selected = !selected;
			selectedCopies[card.id] = 1;
		}
	}

	$: updateCheckbox(selectedCards);

	selectedCopies[card.id] = 1;
	function handleNumberOfCardsChange(event: Event) {
		const input = event.target as HTMLInputElement;
		selectedCopies[card.id] = Number(input.value);
	}
</script>

<tr>
	<script lang="ts">
		import Checkbox from '$lib/components/Checkbox.svelte';
	</script>

	<td class="checkbox-cell">
		<div class="checkbox-wrapper">
			<Checkbox checked={selected} onChange={(val) => handleCheckboxChange(val)} />
			{#if selected}
				<input
					type="number"
					class="cards-number"
					min="1"
					value={selectedCopies[card.id]}
					on:change={(e) => handleNumberOfCardsChange(e)}
				/>
			{/if}
		</div>
	</td>
	<td><a href="/card/{card.id}"><b>{card.name}</b></a></td>
	<td>{cardAuthor}</td>
	<td>{cardType}</td>
</tr>

<style>
	.checkbox-cell {
		width: 80px;
		min-width: 80px;
		max-width: 80px;
		padding: 0;
		padding-left: 11px;
		text-align: left;
	}

	.checkbox-wrapper {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 6px 4px;
		box-sizing: border-box;
	}

	.cards-number {
		width: 38px;
		font-size: 0.9em;
		padding: 3px 4px;
		border-radius: 5px;
		text-align: center;
		background-color: #222831;
		color: #00adb5;
		border: 1px solid #00adb5;
		outline: none;
		flex-shrink: 0;
		appearance: textfield;
	}

	/* Remove spin buttons (Chrome, Safari) */
	.cards-number::-webkit-outer-spin-button,
	.cards-number::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	/* Remove spin buttons (Firefox) */
	.cards-number[type='number'] {
		-moz-appearance: textfield;
	}
</style>
