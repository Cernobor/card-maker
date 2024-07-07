<script lang="ts">
    export let cardName: string;
    export let cardID: number;
    export let cardAuthor: string;
    export let cardType: string;
</script>

<tr>
    <a href="/card/{cardID}">
        <td><b>{cardName}</b></td>
        <td>{cardAuthor}</td>
        <td>{cardType}</td>
    </a>
</tr>