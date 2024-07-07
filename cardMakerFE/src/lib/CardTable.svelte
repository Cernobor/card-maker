<script lang="ts">
	import TableRow from "./TableRow.svelte";
    import Card from '$lib/Card.svelte';

    export let cards: Card[];
</script>

<div>
    <table>
        <tr>
            <th>Karta</th>
            <th>Autor</th>
            <th>Typ</th>
        </tr>
        {#each cards as card}
            <TableRow
                cardName={card.name}
                cardID={card.id}
                cardAuthor={card.author}
                cardType={card.type}
            />
        {/each}
    </table>
</div>