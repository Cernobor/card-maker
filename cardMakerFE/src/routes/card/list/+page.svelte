<script lang="ts">
    import FilterDropdown from "$lib/FilterDropdown.svelte";
	import TableRow from "$lib/TableRow.svelte";
    import Card from '$lib/Card.svelte';
    import type { Author, CardType } from "$lib/types";
    import { fetchCards, fetchAuthors, fetchTypes } from "$lib/fetchResource";
	import { onMount } from "svelte";


    function getFilteredCards(allCards: Card[]|[], selectedAuthor: Author|null, selectedType: CardType|null) {
        let cards = allCards;
        if (selectedAuthor != null) {
            cards = cards.filter((card: Card) => {
                return card.user_id === selectedAuthor.id;
            });
        }
        if (selectedType != null) {
            cards = cards.filter((card: Card) => {
                return card.card_type_id === selectedType.id;
            });
        }
        return cards;
    }

    let allCards: Card[]|[] = [];
    let authors: Author[]|[] = [];
    let types: CardType[]|[] = [];
    
    onMount(async () => {
        allCards = await fetchCards();
        authors = await fetchAuthors();
        types = await fetchTypes();
    });

    let selectedAuthor: Author|null = null;
    let selectedType: CardType|null = null;

    let filteredCards: Card[] = allCards;
    $: filteredCards = getFilteredCards(allCards, selectedAuthor, selectedType);

</script>


<h1>card list</h1>

<div>
    <FilterDropdown bind:selected={selectedAuthor} filterName="Autor" options={authors}/>
    <FilterDropdown bind:selected={selectedType} filterName="Typ karty" options={types}/>
    <div>
        <table>
            <tr>
                <th>Karta</th>
                <th>Autor</th>
                <th>Typ</th>
            </tr>
            {#each filteredCards as card}
                <TableRow
                    card={card}
                    authors={authors}
                    types={types}
                />
            {/each}
        </table>
    </div>
</div>