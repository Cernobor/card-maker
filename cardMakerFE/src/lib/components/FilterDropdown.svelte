<script lang="ts">
    import type { UserPublic, CardType } from "$lib/interfaces";
    export let options: UserPublic[]|CardType[]|[];
    export let selected: UserPublic|CardType|null;
    export let filterName: string;
</script>

<div>
    <h3 class="filter-title">{filterName}</h3>
    <select bind:value={selected}>
        <option value={null}>Vše</option>
        {#each options as optionValue}
            <option value={optionValue}>{optionValue.username}</option>
        {/each}
    </select>
</div>