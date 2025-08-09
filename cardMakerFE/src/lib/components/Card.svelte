<script lang="ts">
	import { slugify } from '$lib/slugify';
	import html2canvas from 'html2canvas';
	import DOMPurify from 'isomorphic-dompurify';
	import { goto } from '$app/navigation';
	import { api } from '$lib/stores/store';
	import type { CardCreate, CardGet, Mode, FlashMessage, ColorType } from '$lib/interfaces';
	import { cardTypeClass, Color } from '$lib/interfaces';
	import type { CardTypeKey, CardTypeClass, CardType } from '$lib/interfaces';
	import jsPDF from 'jspdf';
	import { tick } from 'svelte';
	import { createEventDispatcher } from 'svelte';

	export let mode: Mode = 'create';
	export let card: CardCreate | CardGet;
	export let cardId: number | null = null;
	export let cardTypes: CardType[];

	// Emit flash messages to parent
	const dispatch = createEventDispatcher<{ flash: FlashMessage }>();
	function flash(message: string, color: ColorType) {
		dispatch('flash', { message, color, id: Date.now() + Math.random() });
	}

	export async function save(download: boolean, format?: string, copies?: number) {
		await tick();
		if (download) {
			await downloadCard(format, copies);
		}
		await sentCardToAPI();
	}

	async function generateCardPng(): Promise<string> {
		const capture = document.querySelector('#capture') as HTMLElement;
		const scale = 12;
		const canvas = await html2canvas(capture, {
			useCORS: true,
			onclone: (doc) => {
				const newCapture = doc.querySelector('#capture') as HTMLElement;
				newCapture.style.transform = `scale(${scale})`;
			}
		});
		return canvas.toDataURL('image/png');
	}

	function createPdfFromImage(imgData: string, copies: number): void {
		const pdf = new jsPDF({ orientation: 'l', unit: 'mm', format: 'a4' });
		const pageWidth = 297;
		const pageHeight = 210;
		const margin = 5;

		const capture = document.querySelector('#capture') as HTMLElement;
		const PX_TO_MM = 25.4 / 96;
		const width = capture.offsetWidth * PX_TO_MM;
		const height = capture.offsetHeight * PX_TO_MM;

		let x = margin;
		let y = margin;
		let rowHeight = 0;

		for (let copy = 0; copy < copies; copy++) {
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

		pdf.save(slugify(card.name) + '-card.pdf');
	}

	export async function downloadCard(format?: string, copies: number = 1) {
		const imgData = await generateCardPng();

		if (format === 'pdf') {
			createPdfFromImage(imgData, copies);
			return;
		}

		const a = document.createElement('a');
		a.href = imgData.replace('image/png', 'image/octet-stream'); // prevent DOM 18 error
		a.download = slugify(card.name) + '-card.png';
		document.body.appendChild(a);
		a.click();
		a.remove();
	}

	export async function sentCardToAPI() {
		/**
		 * Send POST or PUT request to API.
		 */
		if (mode == 'create') {
			try {
				await $api.createCard(card);
				flash('✅ Karta byla úspěšně vytvořena.', Color.green);
				goto('/card/list?created=true');
			} catch {
				flash('❌ Oops, kartu se nepodařilo uložit.', Color.red);
			}
		} else if (mode == 'update') {
			if (!cardId) {
				flash('❌ Oops, kartu se nepodařilo uložit.', Color.red);
				return;
			}
			try {
				await $api.updateCard(card, cardId);
				flash('✅ Karta byla úspěšně upravena.', Color.green);
			} catch {
				flash('❌ Oops, kartu se nepodařilo uložit.', Color.red);
			}
		}
	}

	function cardTextFilter(text: string): string {
		/**
		 * Replace special symbols with corresponding html tags.
		 * @param text - text to be filtered
		 */
		text = text
			.replace(/\$uhurus/g, '<span class="lingua-prima">A</span>')
			.replace(/\$donozoros/g, '<span class="lingua-prima">B</span>')
			.replace(/\$zalaras/g, '<span class="lingua-prima">C</span>')
			.replace(/\$miniris/g, '<span class="lingua-prima">D</span>')
			.replace(/\$tenemenes/g, '<span class="lingua-prima">E</span>');

		return text;
	}

	function tagsContainTagName(tagName: string): boolean {
		/**
		 * Compare given tag with card tags
		 * and return true if card has tags else false
		 */
		for (const cardTag of card.tags) {
			if (cardTag.name === tagName) {
				return true;
			}
		}
		return false;
	}

	let cardTypeName: string;
	let cardTypeNameClass: string;
	let cssClass: CardTypeClass = cardTypeClass['Magický předmět'];

	$: if (cardTypes && card) {
		let currentCardType = cardTypes.find((cardType) => {
			return cardType.id == card.card_type_id;
		});
		if (currentCardType) {
			if (currentCardType.name == 'Lokace') {
				cardTypeNameClass = currentCardType.name + '-' + card.size;
				cardTypeName = currentCardType.name;

				cssClass = cardTypeClass[cardTypeNameClass as CardTypeKey];
			} else if (currentCardType.name === "Zaříkadlo" || currentCardType.name === "Recept") {
				if (!card.size) {
					card.size = "small";
				}
				cardTypeNameClass = currentCardType.name + "-" + card.size;
				cardTypeName = currentCardType.name;

				cssClass = cardTypeClass[cardTypeNameClass as CardTypeKey];
			}else {
				cardTypeName = currentCardType.name;
				cssClass = cardTypeClass[cardTypeName as CardTypeKey];
			}

			console.log(cssClass);
		}
	}

	$: card.tags;
</script>

<div
	class="{cssClass} {cardTypeName === 'Lokace' ? 'vertical-center' : 'normal'} card"
	id="capture"
>
	<section class="card-header">
		<div class="card-name">{card.name}</div>
		<div class="card-set">
			{#if cardTypeName == 'Magický předmět' || cardTypeName == 'Volný aspekt'}
				<div class="card-in-set">{card.in_set ? card.set_name : ''}</div>
			{/if}
		</div>
		{#if cardTypeName != 'Lokace'}
			<div class="card-type">{cardTypeName}</div>
		{/if}

		{#if cardTypeName == 'Magický předmět'}
			{#if card.tags.find((tag) => tag.name === 'Neodložitelný')}
				<div class="irremovable">Neodložitelný</div>
			{/if}
		{/if}
	</section>

	<div class="card-body">
		<section class="card-content {cardTypeName === 'Lokace' ? 'location-text' : ''}">
			<div class="card-fluff">
				{@html cardTextFilter(DOMPurify.sanitize(card.fluff || ''))}
			</div>
			<div class="card-effect">
				{@html cardTextFilter(DOMPurify.sanitize(card.effect || ''))}
			</div>
		</section>
	</div>
</div>

<style>
	.card {
		font-size: 8pt;
		background-clip: border-box;
		page-break-after: auto;
		page-break-inside: avoid;
		background-color: white;
	}
	.card-magical-item {
		width: calc(95mm);
		height: calc(75mm);
		border: 2mm solid black;
		font-size: 10pt;
	}
	.card-free-aspect {
		width: calc(75mm);
		height: calc(95mm);
		border: 2mm solid black;
		font-size: 10pt;
	}
	.card-location-large {
		height: 7in;
		width: 290mm;
		font-size: 12pt;
	}
	.card-location-medium {
		height: calc(4in);
		width: calc(290mm);
		font-size: 12pt;
	}
	.card-location-small {
		height: calc(2.2in);
		width: calc(290mm);
		font-size: 12pt;
	}
	.card-recipe {
		width: calc(75mm);
		height: calc(100mm);
		border: 2mm solid black;
		font-size: 10pt;
	}
	.card-spell {
		width: calc(75mm);
		height: calc(100mm);
		border: 2mm solid black;
		font-size: 10pt;
	}
	.card-recipe-large {
		width: calc(120mm);
		height: calc(100mm);
		border: 2mm solid black;
		font-size: 10pt;
	}
	.card-spell-large {
		width: calc(120mm);
		height: calc(100mm);
		border: 2mm solid black;
		font-size: 10pt;
	}
	.card-header {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		border-bottom: 2px solid black;
		gap: 2px;
	}
	.card-location-small .card-name {
		font-size: 60pt;
	}
	.card-location-medium .card-name {
		font-size: 60pt;
	}
	.card-location-large .card-name {
		font-size: 60pt;
	}
	.card-name {
		font-family: 'Inknut Antiqua', serif;
		font-size: 10pt;
		line-height: 1.7em;
		font-weight: bold;
		font-variant: small-caps;
	}
	.card-type {
		font-family: 'Montserrat', sans-serif;
		font-size: 8pt;
		font-weight: 8;
	}
	.card-content div {
		padding: 5px;
		text-align: justify;
		text-align-last: center;
	}
	.card-fluff {
		font-style: italic;
		font-weight: lighter;
	}
	.card-set {
		text-align: center;
		font-size: 6pt;
	}
	.location-text {
		padding-left: 10%;
		padding-right: 10%;
	}
	:global(section.content p) {
		padding-bottom: 2pt;
		margin: 0;
	}
	:global(img.activity) {
		max-height: 8pt;
	}
</style>
