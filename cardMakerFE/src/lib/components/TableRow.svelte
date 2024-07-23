<script lang="ts">
    import type { Author, CardType } from "$lib/types";
    import Card from "./Card.svelte";

    export let card: Card;

    export let authors: Author[]|[];
    export let types: CardType[]|[];

    let cardAuthor: string = "waiting...";
    let cardType: string = "waiting...";

    async function getUserNameByID(id: number) {
        return authors.filter((author) => author.id == id)[0];
    }

    async function getTypeNameByID(id: number) {
        return types.filter((type) => type.id == id)[0];
    }

    $: if (authors.length) {
        (async () => {
            const response = await getUserNameByID(card.user_id);
            cardAuthor = response.name;
        })();
    }
    $: if (types.length) {
    (async () => {
        const response = await getTypeNameByID(card.card_type_id);
        cardType = response.name;
    })();
    }
</script>

<tr>
    <td><a href="/card/{card.id}"><b>{card.name}</b></a></td>
    <td>{cardAuthor}</td>
    <td>{cardType}</td>
</tr>
