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
    <h3>Tagy</h3>
    {#each options as option}
        <label>{option.name}</label>
        <input type="checkbox" value={option.name} on:change={handleChange} />
    {/each}
</div>