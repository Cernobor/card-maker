<script lang="ts">
	import FilterDropdown from '$lib/components/FilterDropdown.svelte';
	import TableRow from '$lib/components/TableRow.svelte';
	import type { CardGet, UserPublic, CardType, Tag } from '$lib/interfaces';
	import FilterLabels from '$lib/components/FilterLabels.svelte';
	import { api } from '$lib/stores/store';

	function getFilteredCards(
		allCards: CardGet[] | [],
		selectedAuthor: UserPublic | null,
		selectedType: CardType | null,
		activeTags: Tag[]
	) {
		/**
		 * Filter cards array according to selected parameters.
		 *
		 * @param allCards - array of CardGet objects (all cards in database)
		 * @param selectedAuthor - UserPublic object
		 * 						(if null, all authors are selected)
		 * @param selectedType - CardType object
		 * 						(if null, all card types are selected)
		 * @param activeTags - array of Tag objects
		 * 						(if empty, all tags are selected)
		 *
		 * @returns array of filtered cards
		 */
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
			for (const activeTag of activeTags) {
				cards = cards.filter((card: CardGet) => {
					for (const cardTag of card.tags) {
						if (cardTag.name === activeTag.name) {
							return true;
						}
					}
					return false;
				});
			}
		}
		return cards;
	}

	let allCards: CardGet[] = [];
	let users: UserPublic[] = [];
	let types: CardType[] = [];
	let tags: Tag[] = [];
	let activeTags: Tag[] = [];

	async function getResources() {
		/**
		 * Get resources from API.
		 */
		allCards = await $api.getCards();
		users = await $api.getUsers();
		types = await $api.getCardTypes();
		tags = await $api.getTags();
	}

	let selectedAuthor: UserPublic | null = null;
	let selectedType: CardType | null = null;

	let filteredCards: CardGet[] = allCards;
	$: filteredCards = getFilteredCards(allCards, selectedAuthor, selectedType, activeTags);
</script>

<div class="card-list-body">
	<div class="filters">
		<FilterDropdown bind:selected={selectedAuthor} filterName="Autor" options={users} />
		<FilterDropdown bind:selected={selectedType} filterName="Typ karty" options={types} />
		<FilterLabels bind:activeTags options={tags} />
	</div>
	<div class="card-list-table">
		<table>
			<tr>
				<th>Karta</th>
				<th>Autor</th>
				<th>Typ</th>
			</tr>
			{#await getResources()}
			
				<h1 style="text-align:center">loading...</h1>
			{:then}

				{#each filteredCards as card}
					<TableRow {card} {users} {types} />
				{/each}
				{#if filteredCards.length === 0}
				<tr>
					<td colspan="3">
						<h1 style="text-align:center">Žádné karty nenalezeny</h1>
					</td>
				</tr>
			   {/if}
			{/await}
		
	</div>
</div>
