<script lang="ts">
    import type { Tag } from "$lib/types";
    export let options: Tag[]|[];
    export let activeTags: number[]|[];

    function handleChange(e) {
        if (e.target.checked) {
            activeTags = [...activeTags, e.target.value];
        } else {
            activeTags = activeTags.filter((_, i) => i !== activeTags.indexOf(e.target.value));
        }
    }
</script>

<div>
    <h3 class="filter-title">Tagy</h3>
    <div class="all-checkboxes-container">
        {#each options as option}
        <div class="checkbox-container" >
            <label for={option.name}>{option.name}</label>
            <input type="checkbox" id={option.name} class="checkbox" value={option.name} on:change={handleChange} />
        </div>
    {/each}
    </div>
</div>