<script lang="ts">
    import FilterDropdown from "$lib/FilterDropdown.svelte";
	import CardTable from "$lib/CardTable.svelte";
    import Card from '$lib/Card.svelte';
    import type { Author, CardType } from "$lib/types";
    import { fetchCards, fetchAuthors, fetchTypes } from "$lib/fetchResource";
	import { onMount } from "svelte";


    function getFilteredCards(allCards: Card[]|[], selectedAuthor: Author|null, selectedType: CardType|null) {
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
    </div>
<CardTable cards={filteredCards}/>