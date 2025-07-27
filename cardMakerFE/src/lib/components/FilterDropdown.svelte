<script lang="ts">
	import type { UserPublic, CardType } from '$lib/interfaces';
	import { isUserPublic } from '$lib/interfaces';
	export let options: UserPublic[] | CardType[];
	export let selected: UserPublic | CardType | null;
	export let filterName: string;
</script>

<div>
	<label for={filterName}>{filterName}</label>
	<select id={filterName} bind:value={selected}>
		<option value={null}>Vše</option>
		{#each options as optionValue}
			{#if isUserPublic(optionValue)}
				<option value={optionValue}>{optionValue.username}</option>
			{:else}
				<option value={optionValue}>{optionValue.name}</option>
			{/if}
		{/each}
	</select>
</div>
