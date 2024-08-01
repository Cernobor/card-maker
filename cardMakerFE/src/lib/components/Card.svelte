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

	export function downloadCard() {
		/**
		 * Download card as png image.
		 */
		html2canvas(document.querySelector('#capture')!).then((canvas) => {
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

	function pfFilter(text: string) {
		text = text
			.replace('$uhurus', '<p class="lingua-prima">A</p>')
			.replace('$donozoros', '<p class="lingua-prima">B</p>')
			.replace('$zalaras', '<p class="lingua-prima">C</p>')
			.replace('$miniris', '<p class="lingua-prima">D</p>')
			.replace('$tenemenes', '<p class="lingua-prima">E</p>');

		return text;
	}

	let cardTypeName: string;
	let cssClass: CardTypeClass = cardTypeClass['Magický předmět'];
	$: if (cardTypes && card) {
		let currentCardType = cardTypes.find((cardType) => {
			return cardType.id == card.card_type_id;
		});
		if (currentCardType) {
			cardTypeName = currentCardType.name;
			cssClass = cardTypeClass[cardTypeName as CardTypeKey];
		}
	}
</script>

<div class="{cssClass} card" id="capture">
	<section class="card-header">
		<div class="card-name">{card.name}</div>
		<div class="card-set">
			{#if cardTypeName == 'Magický předmět' || cardTypeName == 'Volný aspekt'}
				<div class="card-in-set">{card.in_set ? card.set_name : ''}</div>
			{/if}
		</div>
		<div class="card-type">{cardTypeName}</div>
		{#if cardTypeName == 'Magický předmět'}
			<div class="irremovable">
				{card.tags.includes({ name: 'Neodložitelný' }) ? 'Neodložitelný' : ''}
			</div>
		{/if}
	</section>

	<div class="card-body">
		<section class="card-content">
			<div class="card-fluff">
				{@html pfFilter(DOMPurify.sanitize(card.fluff || ''))}
			</div>
			<div class="card-effect">
				{@html pfFilter(DOMPurify.sanitize(card.effect || ''))}
			</div>
		</section>
	</div>
</div>

<style>
	.card {
		width: calc(2.5in - 4mm);
		height: calc(3.5in - 4mm);
		font-size: 8pt;
		border: 2mm solid black;
		background-clip: border-box;
		page-break-after: auto;
		page-break-inside: avoid;
		background-color: white;
	}

	.card-magical-item {
		height: calc(2.5in - 4mm);
		width: calc(3.5in - 4mm);
	}
	.card-free-aspect {
		width: calc(2.5in - 4mm);
		height: calc(3.5in - 4mm);
	}
	.card-location {
		height: calc(7in);
		width: calc(10in);
	}
	.card-header {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		border-bottom: 2px solid black;
		gap: 2px;
	}
	.card-name {
		font-family: 'Inknut Antiqua', serif;
		font-size: 10pt;
		line-height: 1.7em;
		font-weight: bold;
		text-transform: capitalize;
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
	:global(section.content p) {
		padding-bottom: 2pt;
		margin: 0;
	}
	:global(img.activity) {
		max-height: 8pt;
	}
</style>
