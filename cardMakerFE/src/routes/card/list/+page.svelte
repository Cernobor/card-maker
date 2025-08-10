<script lang="ts">
	import { onMount, tick } from 'svelte';
	import html2canvas from 'html2canvas';
	import jsPDF from 'jspdf';
	import { fade } from 'svelte/transition';
	import TableRow from '$lib/components/TableRow.svelte';
	import {
		type CardGet,
		type UserPublic,
		type CardType,
		type Tag,
		type ColorType,
		Color,
		type FlashMessage,

		cardTypeClass

	} from '$lib/interfaces';
	import { api } from '$lib/stores/store';
	import Card from '$lib/components/Card.svelte';
	import Checkbox from '$lib/components/Checkbox.svelte';
	import PdfPreviewModal from '$lib/components/PdfPreviewModal.svelte';
	import PopUpMessage from '$lib/components/PopUpMessage.svelte';
	import Filters from '$lib/components/Filters.svelte';
	import { goto } from '$app/navigation';

	function getFilteredCards(
		allCards: CardGet[] | [],
		selectedAuthor: UserPublic | null,
		selectedType: CardType | null,
		activeTags: Tag[],
		search: string
	) {
		/**
		 * Filter cards array according to selected parameters.
		 *
		 * @param allCards - array of CardGet objects (all cards in database)
		 * @param selectedAuthor - UserPublic object
		 * 						(if null, all authors are selected)
		 * @param selectedType - CardType object
		 * 						(if null, all card types are selected)
		 * @param activeTags - array of Tag objects
		 * 						(if empty, all tags are selected)
		 *
		 * @returns array of filtered cards
		 */
		let cards = allCards;
		if (selectedAuthor != null) {
			cards = cards.filter((card: CardGet) => {
				return card.user_id === selectedAuthor.id;
			});
		}
		if (selectedType != null) {
			cards = cards.filter((card: CardGet) => {
				return card.card_type_id === selectedType.id;
			});
		}
		if (activeTags.length > 0) {
			for (const activeTag of activeTags) {
				cards = cards.filter((card: CardGet) => {
					for (const cardTag of card.tags) {
						if (cardTag.name === activeTag.name) {
							return true;
						}
					}
					return false;
				});
			}
		}
		if (search !== '') {
			cards = cards.filter((c) => {
				return c.name.toLocaleLowerCase().includes(search.toLocaleLowerCase());
			});
		}
		return cards;
	}

	let allCards: CardGet[] = [];
	let users: UserPublic[] = [];
	let types: CardType[] = [];
	let tags: Tag[] = [];
	const year = new Date().getFullYear().toString();
	let activeTags: Tag[] = [{ name: year }];
	let search: string = '';

	async function getResources() {
		/**
		 * Get resources from API.
		 */
		allCards = await $api.getCards();
		users = await $api.getUsers();
		types = await $api.getCardTypes();
		tags = await $api.getTags();
	}

	let selectedAuthor: UserPublic | null = null;
	let selectedType: CardType | null = null;

	let filteredCards: CardGet[] = allCards;
	$: filteredCards = getFilteredCards(allCards, selectedAuthor, selectedType, activeTags, search);

	let flashMessages: FlashMessage[] = [];
	export let data: { cardCreated: boolean };

	function pushFlash(message: string, color: ColorType) {
		const item = { message, color, id: Date.now() + Math.random() };
		flashMessages = [...flashMessages, item];
		setTimeout(() => {
			flashMessages = flashMessages.filter((m) => m.id !== item.id);
		}, 4000);
	}

	onMount(() => {
		flashMessages = [];
		if (data.cardCreated) {
			pushFlash('✅ Karta byla úspěšně vytvořena.', Color.green);
			goto('/card/list', { replaceState: true, noScroll: true });
		}
	});

	$: flashMessages;

	let selectedCards: CardGet[] = [];

	function handleSelectedCardsChange() {
		const previousCount = selectedCards.length;
		const updatedSelectedCards = selectedCards.filter((card: CardGet) =>
			filteredCards.includes(card)
		);
		const removedCount = previousCount - updatedSelectedCards.length;
		if (removedCount > 0) {
			pushFlash(
				`ℹ️ ${removedCount} ${removedCount === 1 ? 'karta byla' : 'karet bylo'} odstraněno z výběru kvůli filtru.`,
				Color.blue
			);
		}

		selectedCards = updatedSelectedCards;
	}

	$: if (filteredCards || selectedCards) {
		handleSelectedCardsChange();
	}

	let checkedAll = false;

	function handleCheckboxChange(checked: boolean) {
		if (checked) {
			selectedCards = filteredCards;
			checkedAll = true;
		} else {
			selectedCards = [];
			checkedAll = false;
		}
	}

	let isBusy: boolean = false;
	let selectedCopies: Record<number, number> = {};

	async function createPdf(
		cards: CardGet[],
		selectedCopies: Record<number, number>
	): Promise<jsPDF> {
		isBusy = true;
		await tick();

		const locationCardTtype = types.filter(t => {
			return t.name === "Lokace"
		})[0];

		const locationInCards = cards.filter(c => {
			console.log(c.card_type_id);
			return c.card_type_id === locationCardTtype.id;
		}).length > 0;

		const pageOrientation = locationInCards ? "l" : "p";
		const pdf = new jsPDF({ orientation: pageOrientation, unit: 'mm', format: 'a4' });
		const pageWidth = locationInCards ? 297 : 210;
		const pageHeight = locationInCards ? 210 : 297;
		const margin = 1;

		let x = 5*margin;
		let y = 5*margin;
		let rowHeight = 0;

		for (const card of cards) {
			const copies = selectedCopies[card.id] ?? 1;

			for (let copy = 0; copy < copies; copy++) {
				const el = document.getElementById(`card-${card.id}`);
				if (!el) {
					console.warn(`Element card-${card.id} not found`);
					continue;
				}

				const canvas = await html2canvas(el, { scale: 4, useCORS: true });
				const imgData = canvas.toDataURL('image/png');

				const PX_TO_MM = 25.4 / 96;
				const width = el.offsetWidth * PX_TO_MM;
				const height = el.offsetHeight * PX_TO_MM;

				if (x + width + 5*margin > pageWidth) {
					x = 5*margin;
					y += rowHeight + margin;
					rowHeight = 0;
				}

				if (y + height + 5*margin > pageHeight) {
					pdf.addPage();
					x = 5*margin;
					y = 5*margin;
					rowHeight = 0;
				}

				pdf.addImage(imgData, 'PNG', x, y, width, height);

				x += width + margin;
				if (height > rowHeight) rowHeight = height;
			}
		}

		isBusy = false;
		return pdf;
	}

	let showPdfModal = false;
	let pdfBlobUrl: string | null = null;

	let previewButton: HTMLButtonElement;

	async function showPreview() {
		const pdf = await createPdf(selectedCards, selectedCopies);
		const blob = pdf.output('blob');
		pdfBlobUrl = URL.createObjectURL(blob);
		previewButton?.blur();
		showPdfModal = true;
	}

	async function downloadCards(pdf?: jsPDF) {
		if (!pdf) {
			pdf = await createPdf(selectedCards, selectedCopies);
		}
		pdf.save('cards.pdf');
		selectedCards = [];
		checkedAll = false;
	}
</script>

<div class="card-list-body">
	<div class="flash-message-wrapper">
		{#each flashMessages as message (message.id)}
			<div class="pop-up-wrapper" in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
				<PopUpMessage
					{message}
					on:close={() => {
						flashMessages = flashMessages.filter((m) => m !== message);
					}}
				/>
			</div>
		{/each}
	</div>

	<h2 class="page-name">🗂️ Seznam karet</h2>

	<Filters
		bind:search
		bind:selectedAuthor
		bind:selectedType
		bind:activeTags
		{users}
		{types}
		{tags}
	/>

	<div class={`card-table-actions ${selectedCards.length > 0 ? 'actions-active' : ''}`}>
		<button
			on:click={() => {
				selectedCards = [];
				checkedAll = false;
			}}
			class="cancel-button"
			disabled={selectedCards.length === 0}>❌</button
		>
		<span>
			{selectedCards.length === 0
				? 'Žádná karta nevybrána'
				: `${selectedCards.length} ${
						selectedCards.length === 1
							? 'karta vybrána'
							: selectedCards.length >= 2 && selectedCards.length <= 4
								? 'karty vybrány'
								: 'karet vybráno'
					}`}
		</span>
		<button on:click={showPreview} bind:this={previewButton} disabled={selectedCards.length === 0}
			>👁️ Náhled</button
		>
		<button on:click={() => downloadCards()} disabled={selectedCards.length === 0}
			>⬇️ Stáhnout vybrané</button
		>
	</div>

	<div class="card-list-table">
		<table>
			<tr>
				<th class="checkbox-column">
					<Checkbox checked={checkedAll} onChange={handleCheckboxChange} />
				</th>
				<th>Karta</th>
				<th>Autor</th>
				<th>Typ</th>
			</tr>
			{#await getResources()}
				<h1 style="text-align:center">loading...</h1>
			{:then}
				{#each filteredCards as card}
					<TableRow {card} {users} {types} bind:selectedCards bind:selectedCopies />
				{/each}
				{#if filteredCards.length === 0}
					<tr>
						<td colspan="4">
							<h1 style="text-align:center">Žádné karty nenalezeny</h1>
						</td>
					</tr>
				{/if}
			{/await}
		</table>
	</div>

	<div class="card-pdf-render" aria-hidden="true">
		{#each selectedCards as card}
			<span id={'card-' + card.id}>
				<Card {card} cardTypes={types} mode="preview" />
			</span>
		{/each}
	</div>

	{#if isBusy}
		<div class="spinner-overlay">
			<div class="lds-dual-ring"></div>
		</div>
	{/if}

	<PdfPreviewModal
		open={showPdfModal}
		blobUrl={pdfBlobUrl}
		onClose={() => (showPdfModal = false)}
	/>
</div>

<style>
	.card-list-table th {
		padding: 8px 12px;
		font-family: 'Inknut Antiqua', serif;
		line-height: 85%;
	}

	.card-list-table th:first-child {
		width: 80px;
		min-width: 80px;
		max-width: 80px;
		text-align: left;
		padding-left: 15px;
		box-sizing: border-box;
	}

	.card-table-actions {
		display: flex;
		justify-content: center;
		align-items: center;
		flex-wrap: wrap;
		gap: 0.75rem;
		margin: 1rem;
		background-color: #161a20;
		padding: 0.75rem 1rem;
		opacity: 0.5;
		transition: opacity 0.5s ease;
		border-radius: 12px;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
		z-index: 1;
		font-family: 'Inknut Antiqua', serif;
		line-height: 85%;
	}

	.actions-active {
		opacity: 1;
	}

	.card-table-actions button {
		cursor: not-allowed;
		transition: background-color 0.2s ease;
		font-family: 'Inknut Antiqua', serif;
		line-height: 85%;
	}

	.actions-active button {
		cursor: pointer;
	}

	.card-table-actions button:hover {
		background-color: #161a20;
	}

	.card-table-actions button:hover:disabled {
		background-color: #24282e;
	}

	.card-table-actions .cancel-button:hover {
		background-color: transparent;
	}

	.card-pdf-render {
		color: black;
		position: absolute;
		top: -9999px;
		left: 0;
		opacity: 0;
		pointer-events: none;
		width: 0;
		height: 0;
	}

	.spinner-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 9999;
	}

	.lds-dual-ring {
		display: inline-block;
		width: 80px;
		height: 80px;
	}

	.lds-dual-ring:after {
		content: ' ';
		display: block;
		width: 64px;
		height: 64px;
		margin: 8px;
		border-radius: 50%;
		border: 6px solid #00adb5;
		border-color: #00adb5 transparent #00adb5 transparent;
		animation: lds-dual-ring 1.2s linear infinite;
	}

	@keyframes lds-dual-ring {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.pop-up-wrapper {
		justify-content: center;
		display: flex;
		margin-top: 15px;
	}

	.above-the-table {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		align-items: flex-start;
		background-color: #161a20;
		padding: 1.25rem 1.5rem;
		border-radius: 12px;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
		gap: 1.5rem;
		margin: 1.5rem 1rem;
	}

	.filters-wrapper {
		display: flex;
		flex-direction: column;
		flex-grow: 1;
	}

	.filters {
		display: flex;
		flex-wrap: nowrap;
		align-items: flex-end;
		gap: 1.25rem;
		align-items: center;
		padding-top: 10px;
	}

	.filter-heading {
		grid-column: 1 / -1;
		margin-bottom: 0.25rem;
		font-size: 1.3rem;
		font-weight: 600;
		color: #eeeeee;
		border-bottom: 2px solid #00adb5;
		padding-bottom: 0.2rem;
		font-family: 'Inknut Antiqua', serif;
	}

	.page-buttons {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		font-family: 'Inknut Antiqua', serif;
	}

	.card-list-body {
		align-items: center;
		margin-bottom: 0;
		padding-bottom: 0;
	}

	.card-list-table {
		width: 100%;
		margin: 0;
		padding: 0;
	}
	.card-list-table table {
		width: 100%;
		table-layout: fixed;
		border-collapse: collapse;
		margin-top: 0;
	}

	.filter-title {
		font-family: 'Inknut Antiqua', serif;
	}

	.filter-tags {
		margin-bottom: 15px;
	}

	.flash-message-wrapper {
		display: block;
		width: 100%;
	}
</style>
