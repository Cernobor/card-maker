<script lang="ts">
	import { slugify } from '$lib/slugify';
	import html2canvas from 'html2canvas';
	import DOMPurify from 'isomorphic-dompurify';
	import { api } from '$lib/stores/store';
	import type { CardCreate, CardGet, Mode } from '$lib/interfaces';
	import { cardTypeClass } from '$lib/interfaces';
	import type { CardTypeKey, CardTypeClass, CardType } from '$lib/interfaces';

	export let mode: Mode = 'create';
	export let card: CardCreate | CardGet;
	export let cardId: number | null = null;
	export let cardTypes: CardType[];

	export function save(download: boolean, format?: string) {
		if (download) {
			downloadCard(format);
		}
		sentCardToAPI();
	}

	export function downloadCard(format?: string) {
		/**
		 * Download card as png image.
		 */
		const capture = document.querySelector('#capture') as HTMLElement;
		const scale = 12;
		html2canvas(capture, {
			onclone: (doc) => {
				console.log(doc);
				const newCapture = doc.querySelector('#capture') as HTMLElement;
				newCapture.style.transform = `scale(${scale})`;
			},
		}).then((canvas) => {

			let a = document.createElement('a');
			a.href = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream'); // here is the most important part because if you dont replace you will get a DOM 18 exception.
			a.download = slugify(card.name) + '-card.png';

			document.body.appendChild(a);
			a.click();
		});
	}

	export async function sentCardToAPI() {
		/**
		 * Send POST or PUT request to API.
		 */
		if (mode == 'create') {
			try {
				await $api.createCard(card);
				alert('Karta byla úspěšně uložena.');
			} catch {
				alert('Oops, kartu se nepodařilo uložit.');
			}
		} else if (mode == 'update') {
			if (!cardId) {
				alert('Oops, kartu se nepodařilo uložit.');
				return;
			}
			try {
				await $api.updateCard(card, cardId);
				alert('Karta byla úspěšně uložena.');
			} catch {
				alert('Oops, kartu se nepodařilo uložit.');
			}
		}
	}

	function cardTextFilter(text: string): string {
		/**
		 * Replace special symbols with corresponding html tags.
		 * @param text - text to be filtered
		 */
		text = text
			.replace('$uhurus', '<p class="lingua-prima">A</p>')
			.replace('$donozoros', '<p class="lingua-prima">B</p>')
			.replace('$zalaras', '<p class="lingua-prima">C</p>')
			.replace('$miniris', '<p class="lingua-prima">D</p>')
			.replace('$tenemenes', '<p class="lingua-prima">E</p>');

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
				cardTypeNameClass = currentCardType.name+"-" +card.size;
				cardTypeName= currentCardType.name

				cssClass = cardTypeClass[cardTypeNameClass as CardTypeKey];
			} else {
				cardTypeName = currentCardType.name;
				cssClass = cardTypeClass[cardTypeName as CardTypeKey];
			}

		console.log(cssClass)
			
		}
	}
</script>

<div class="{cssClass} {(cardTypeName === 'Lokace') ? 'vertical-center' : 'normal'} card" id="capture">

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
			<div class="irremovable">
				{tagsContainTagName('Neodložitelný') ? 'Neodložitelný' : ''}
			</div>
		{/if}
	</section>

	<div class="card-body">
		<section class="card-content {(cardTypeName === 'Lokace') ? 'location-text' : ''}">
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
	}
	.card-free-aspect {
		width: calc(75mm);
		height: calc(95mm);
		border: 2mm solid black;
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
		width: calc(105mm);
		height: calc(115mm);
		border: 2mm solid black;
	}
	.card-spell {
		width: calc(105mm);
		height: calc(115mm);
		border: 2mm solid black;
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
