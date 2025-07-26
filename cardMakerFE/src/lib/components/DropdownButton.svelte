<script lang="ts">
	import type { Format } from '$lib/interfaces';
	import { onMount, onDestroy } from 'svelte';

	export let onSave: (download: boolean, format?: string, copies?: number) => void;

	let showMenu = false;

	let justSaveText = 'Uložit';
	let downloadPdfText = 'Uložit a stáhnout pdf';
	let downloadPngText = 'Uložit a stáhnout png';

	let download: boolean;
	let format: Format;
	let buttonText: string;
	let copies: number;

	let container: HTMLDivElement;

	function handleClickOutside(event: MouseEvent) {
		if (showMenu && container && !container.contains(event.target as Node)) {
			showMenu = false;
		}
	}

	onMount(() => {
		selectJustSave();
		document.addEventListener('click', handleClickOutside);
	});

	onDestroy(() => {
		document.addEventListener('click', handleClickOutside);
	});

	function toggleMenu() {
		showMenu = !showMenu;
	}

	function hideMenu() {
		showMenu = false;
	}

	function selectJustSave() {
		download = false;
		format = undefined;
		buttonText = justSaveText;
		copies = 0;
		hideMenu();
	}

	function selectDownloadPdf() {
		download = true;
		format = 'pdf';
		buttonText = downloadPdfText;
		copies = 1;
		hideMenu();
	}

	function selectDownloadPng() {
		download = true;
		format = 'png';
		buttonText = downloadPngText;
		copies = 0;
		hideMenu();
	}

	function setCopies(event: Event) {
		const input = event.currentTarget as HTMLInputElement;
		copies = Number(input.value);
	}
</script>

<div bind:this={container}>
	<div class="button-group">
		<button class="main-button" on:click={() => onSave(download, format, copies)}>{buttonText}</button>
		<button class="arrow-button" on:click={toggleMenu}>
			{showMenu ? '▲' : '▼'}
		</button>
	</div>
	{#if format === 'pdf'}
		<span class="number-of-copies-wrapper">
			<label for="number-of-copies">Počet kopií karty:</label>
			<input
				type="number"
				id="number-of-copies"
				min="1"
				value={copies}
				on:change={(e) => setCopies(e)}
			/>
		</span>
	{/if}
	{#if showMenu}
		<div class="dropdown">
			<button on:click={selectJustSave}>{justSaveText}</button>
			<button on:click={selectDownloadPdf}>{downloadPdfText}</button>
			<button on:click={selectDownloadPng}>{downloadPngText}</button>
		</div>
	{/if}
</div>

<style>
	.button-group {
		background-color: #31363f;
		color: #eeeeee;
		border-style: outset;
		border-radius: 20px;
		border-color: #00adb5;
		font-size: 16px;
		font-weight: 600;
		padding: 10px;
		border-width: 2px;
	}

	.button-group:hover {
		background-color: #222831;
		cursor: pointer;
	}

	.main-button,
	.arrow-button {
		border: none;
		background-color: transparent;
		padding-top: 0;
		padding-bottom: 0;
	}

	.main-button:hover,
	.arrow-button:hover {
		color: #00adb5;
	}

	.dropdown {
		display: flex;
		flex-direction: column;
		background-color: #222831;
		padding: 10px;
		position: absolute;
		margin-left: 10px;
		border-radius: 5px;
	}

	.dropdown button {
		border: none;
		background-color: transparent;
		text-align: left;
		padding: 2px;
	}

	.dropdown button:hover {
		color: #00adb5;
	}

	.number-of-copies-wrapper {
		display: inline-block;
		padding-top: 10px;
		padding-left: 10px;
		color: white;
	}

	#number-of-copies {
		width: 38px;
		font-size: 0.9em;
		padding: 3px 4px;
		border-radius: 5px;
		text-align: center;
		background-color: #222831;
		color: #00adb5;
		border: 1px solid #00adb5;
		outline: none;
		flex-shrink: 0;
		appearance: textfield;
	}
</style>
