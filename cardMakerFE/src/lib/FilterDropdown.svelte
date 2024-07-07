<script lang="ts">
    import type { Author, CardType } from "$lib/types";
    export let options: Author[]|CardType[]|[];
    export let selected: Author|CardType|null;
    export let filterName: string;
</script>

<div>
    <h3 class="filter-title">{filterName}</h3>
    <select bind:value={selected}>
        <option value={null}>All</option>
        {#each options as optionValue}
            <option value={optionValue}>{optionValue.name}</option>
        {/each}
    </select>
</div>