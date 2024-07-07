<script lang="ts">
    import FilterDropdown from "$lib/FilterDropdown.svelte";
	import CardTable from "$lib/CardTable.svelte";
    import Card from '$lib/Card.svelte';
    import type { Author, CardType } from "$lib/types";
    import { fetchCards, fetchAuthors, fetchTypes } from "$lib/fetchResource";


    function getFilteredCards(allCards: Card[]|[], selectedAuthor: Author, selectedType: CardType) {
        let cards = allCards;
        if (selectedAuthor != null) {
            cards = cards.filter((card: Card) => {
                return card.userID === selectedAuthor.id;
            });
        }
        if (selectedType != null) {
            cards = cards.filter((card: Card) => {
                return card.cardTypeID === selectedType.id;
            });
        }
        return cards;
    }
    
    
    const allCards = fetchCards();
    const authors = fetchAuthors();
    const types = fetchTypes();

    let selectedAuthor: Author|null = null;
    let selectedType: CardType|null = null;

    let filteredCards: Card[];
    $: filteredCards = getFilteredCards(allCards, selectedAuthor, selectedType);

</script>


<h1>card list</h1>

<div>
    <FilterDropdown bind:selected={selectedAuthor} filterName="Autor" options={authors}/>
    <FilterDropdown bind:selected={selectedType} filterName="Typ karty" options={types}/>
    </div>
<CardTable cards={filteredCards}/>