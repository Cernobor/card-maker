<script lang="ts">
	import type { UserPublic, CardType, Tag, CardGet } from '$lib/interfaces';
	import FilterDropdown from './FilterDropdown.svelte';
	import ChangeTagDropdown from './ChangeTagDropdown.svelte';
	import TagLabels from './TagLabels.svelte';

	export let users: UserPublic[] = [];
	export let types: CardType[] = [];
	export let tags: Tag[] = [];

	export let selectedAuthor: UserPublic | null = null;
	export let selectedType: CardType | null = null;
	export let activeTags: Tag[] = [];

	export let search: string = '';

	function handleCancelFilters() {
		selectedAuthor = null;
		selectedType = null;
		activeTags = [];
	}

	function handleSearch(event: Event) {
		const input = event.target as HTMLInputElement;
		search = input.value.trim();
	}
</script>

<div class="above-the-table">
	<div class="filters-left">
		<div class="filters-heading-wrapper">
			<h3 class="filter-heading">🔍 Filtry</h3>
			<div class="filter-line"></div>
		</div>

		<div class="filters">
			<button
				disabled={selectedAuthor === null && selectedType === null && activeTags.length === 0}
				on:click={handleCancelFilters}
				class="cancel-button">❌</button
			>
			<span>
				<label for="search-input">Hledat</label>
				<input on:input={(e) => handleSearch(e)} id="search-input" value={search} />
			</span>
			<FilterDropdown bind:selected={selectedAuthor} filterName="Autor" options={users} />
			<FilterDropdown bind:selected={selectedType} filterName="Typ karty" options={types} />
			<ChangeTagDropdown bind:tags bind:activeTags />
			<TagLabels bind:activeLabels={activeTags} />
		</div>
	</div>

	<!-- <div class="page-buttons">
		<a href="/">ℹ️ Info</a>
		<a href="/card">📄 Nová karta</a>
	</div> -->
</div>

<style>
	input {
		height: 30px;
	}

	.above-the-table {
		display: flex;
		align-items: center;
		justify-content: space-between;
		background-color: #161a20;
		padding: 1rem 1.5rem;
		border-radius: 12px;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
		gap: 2rem;
		margin: 20px;
	}

	.filters-left {
		display: flex;
		flex-direction: column;
		justify-content: center;
		flex-grow: 1;
	}

	.filter-heading {
		font-size: 1.3rem;
		font-weight: 600;
		color: #eeeeee;
		border-bottom: 2px solid #00adb5;
		margin: 0;
		padding-bottom: 0.3rem;
		display: flex;
		align-items: center;
		height: 2rem;
		height: 44px;
		font-family: 'Inknut Antiqua', serif;
		gap: 10px;
	}

	.filters {
		display: flex;
		flex-wrap: nowrap;
		gap: 1.25rem;
		margin-top: 0.5rem;
		height: 44px;
		align-items: center;
	}

	/* .page-buttons {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		padding: 0;
		font-family: 'Inknut Antiqua', serif;
		line-height: 85%;
	}

	.page-buttons a {
		font-family: 'Inknut Antiqua', serif;
		line-height: 85%;
	} */
</style>
