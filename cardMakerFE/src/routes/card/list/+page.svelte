<script lang="ts">
    import FilterDropdown from "$lib/components/FilterDropdown.svelte";
	import TableRow from "$lib/components/TableRow.svelte";
    import Card from '$lib/components/Card.svelte';
    import type { Author, CardType, Tag } from "$lib/types";
    import { fetchCards, fetchAuthors, fetchTypes, fetchTags } from "$lib/fetchResource";
	import { onMount } from "svelte";
	import FilterCheckbox from "$lib/components/FilterCheckbox.svelte";


    function getFilteredCards(allCards: Card[]|[], selectedAuthor: Author|null, selectedType: CardType|null, activeTags: number[]) {
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
        if (activeTags.length > 0) {
            for (const tagName of activeTags) {
                cards = cards.filter((card: Card) => {
                    for (const cardTag of card.tags) {
                        if (cardTag.name === tagName) {
                            return true;
                        }
                    }
                    return false;
                })
            }
        }
        return cards;
    }


    let allCards: Card[]|[] = [];
    let authors: Author[]|[] = [];
    let types: CardType[]|[] = [];
    let tags: Tag[]|[] = [];
    let activeTags: number[]|[] = [];
    
    onMount(async () => {
        allCards = await fetchCards();
        authors = await fetchAuthors();
        types = await fetchTypes();
        tags = await fetchTags();
    });

    let selectedAuthor: Author|null = null;
    let selectedType: CardType|null = null;

    let filteredCards: Card[] = allCards;
    $: filteredCards = getFilteredCards(allCards, selectedAuthor, selectedType, activeTags);
</script>

<div class="card-list-body">
    <div class="filters">
        <FilterDropdown bind:selected={selectedAuthor} filterName="Autor" options={authors}/>
        <FilterDropdown bind:selected={selectedType} filterName="Typ karty" options={types}/>
        <FilterCheckbox bind:activeTags options={tags}/>
    </div>
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