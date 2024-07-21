<script lang="ts">
	import FilterDropdown from '$lib/components/FilterDropdown.svelte';
	import TableRow from '$lib/components/TableRow.svelte';
	import Card from '$lib/components/Card.svelte';
	import type { Author, CardType, Tag } from '$lib/types';
	import { fetchCards, fetchAuthors, fetchTypes, fetchTags } from '$lib/fetchResource';
	import { onMount } from 'svelte';
	import FilterCheckbox from '$lib/components/FilterCheckbox.svelte';
	import { api } from '$lib/stores/store';

	function getFilteredCards(
		allCards: CardGet[] | [],
		selectedAuthor: UserPublic | null,
		selectedType: CardType | null,
		activeTags: number[]
	) {
		let cards = allCards;
		if (selectedAuthor != null) {
			cards = cards.filter((card: CardGet) => {
				return card.user_id === selectedAuthor.id;
			});
		}
		if (selectedType != null) {
			cards = cards.filter((card: CardGet) => {
				return card.card_type_id === selectedType.id;
			});
		}
		if (activeTags.length > 0) {
			for (const tagName of activeTags) {
				cards = cards.filter((card: CardGet) => {
					for (const cardTag of card.tags) {
						if (cardTag.name === tagName) {
							return true;
						}
					}
					return false;
				});
			}
		}
		return cards;
	}

	let allCards: CardGet[] | [] = [];
	let authors: UserPublic[] | [] = [];
	let types: CardType[] | [] = [];
	let tags: Tag[] | [] = [];
	let activeTags: number[] | [] = [];

	onMount(async () => {
		allCards = await $api.getCards();
		authors = await $api.getUsers();
		types = await $api.getCardTypes();
		tags = await $api.getTags();
	});

	let selectedAuthor: UserPublic | null = null;
	let selectedType: CardType | null = null;

	let filteredCards: CardGet[] = allCards;
	$: filteredCards = getFilteredCards(allCards, selectedAuthor, selectedType, activeTags);
</script>

<div class="card-list-body">
	<div class="filters">
		<FilterDropdown bind:selected={selectedAuthor} filterName="Autor" options={authors} />
		<FilterDropdown bind:selected={selectedType} filterName="Typ karty" options={types} />
		<FilterCheckbox bind:activeTags options={tags} />
	</div>
	<div>
		<table>
			<tr>
				<th>Karta</th>
				<th>Autor</th>
				<th>Typ</th>
			</tr>
			{#each filteredCards as card}
				<TableRow {card} {authors} {types} />
			{/each}
		</table>
	</div>
</div>
