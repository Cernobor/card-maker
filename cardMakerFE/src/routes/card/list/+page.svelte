<script lang="ts">
	import { tick } from 'svelte';
	import html2canvas from 'html2canvas';
	import jsPDF from 'jspdf';
	import FilterDropdown from '$lib/components/FilterDropdown.svelte';
	import TableRow from '$lib/components/TableRow.svelte';
	import type { CardGet, UserPublic, CardType, Tag } from '$lib/interfaces';
	import FilterLabels from '$lib/components/FilterLabels.svelte';
	import { api } from '$lib/stores/store';
	import Card from '$lib/components/Card.svelte';

	function getFilteredCards(
		allCards: CardGet[] | [],
		selectedAuthor: UserPublic | null,
		selectedType: CardType | null,
		activeTags: Tag[]
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
		return cards;
	}

	let allCards: CardGet[] = [];
	let users: UserPublic[] = [];
	let types: CardType[] = [];
	let tags: Tag[] = [];
	let activeTags: Tag[] = [];

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
	$: filteredCards = getFilteredCards(allCards, selectedAuthor, selectedType, activeTags);

	let selectedCards: CardGet[] = [];
	$: selectedCards = selectedCards.filter((card: CardGet) => {
		return filteredCards.includes(card);
	});

	function selectAll() {
		selectedCards = filteredCards;
	}

	let isBusy: boolean = false;

	async function createPdf(cards: CardGet[]): Promise<jsPDF> {
		isBusy = true;
		await tick();

		const pdf = new jsPDF({ orientation: 'l', unit: 'mm', format: 'a4' });
		const pageWidth = 297;
		const pageHeight = 210;
		const margin = 5;

		let x = margin;
		let y = margin;
		let rowHeight = 0;

		for (let i = 0; i < cards.length; i++) {
			const el = document.getElementById(`card-${cards[i].id}`);
			if (!el) {
				console.warn(`Element card-${cards[i].id} not found`);
				continue;
			}

			const canvas = await html2canvas(el, { scale: 4, useCORS: true });
			const imgData = canvas.toDataURL('image/png');

			const PX_TO_MM = 25.4 / 96;

			const width = el.offsetWidth * PX_TO_MM;
			const height = el.offsetHeight * PX_TO_MM;

			if (x + width + margin > pageWidth) {
				x = margin;
				y += rowHeight + margin;
				rowHeight = 0;
			}

			if (y + height + margin > pageHeight) {
				pdf.addPage();
				x = margin;
				y = margin;
				rowHeight = 0;
			}

			pdf.addImage(imgData, 'PNG', x, y, width, height);

			x += width + margin;
			if (height > rowHeight) rowHeight = height;
	}
	isBusy = false;
	return pdf;
}

	function showPreview() {

	}

	async function downloadCards(pdf?: jsPDF) {
		if (!pdf) {
			pdf = await createPdf(selectedCards);
		}
		pdf.save("cards.pdf")
	}
</script>

<div class="card-list-body">
	<div class="filters">
		<FilterDropdown bind:selected={selectedAuthor} filterName="Autor" options={users} />
		<FilterDropdown bind:selected={selectedType} filterName="Typ karty" options={types} />
		<FilterLabels bind:activeTags options={tags} />
	</div>

	{#if selectedCards.length > 0}
		<div class="card-table-actions">
			<span>Vybráno {selectedCards.length} karet</span>
			<button on:click={showPreview}>Náhled</button>
			<button on:click={() => downloadCards()}>Stáhnout vybrané</button>
			<button on:click={() => selectedCards = []}>Zrušit výběr</button>
		</div>
	{/if}

	<div class="card-list-table">
		<table>
			<tr>
				<th class="checkbox-column">
					<button on:click={selectAll}>Vybrat vše</button>
				</th>
				<th>Karta</th>
				<th>Autor</th>
				<th>Typ</th>
			</tr>
			{#await getResources()}
			
				<h1 style="text-align:center">loading...</h1>
			{:then}

				{#each filteredCards as card}
					<TableRow {card} {users} {types} bind:selectedCards />
				{/each}
				{#if filteredCards.length === 0}
				<tr>
					<td colspan="3">
						<h1 style="text-align:center">Žádné karty nenalezeny</h1>
					</td>
				</tr>
			   {/if}
			{/await}
		
	</div>

<!-- Skrytý render karet pro PDF export -->
<div class="card-pdf-render" aria-hidden="true">
	{#each selectedCards as card}
	<span id={"card-" + card.id} >
		<Card
			card={card}
			cardTypes={types}
			mode="preview"
		/>
	</span>
	{/each}
</div>

{#if isBusy}
	<div class="spinner-overlay">
		<div class="lds-dual-ring"></div>
	</div>
{/if}

</div>

<style>
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
	content: " ";
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
</style>