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

	export function saveCard() {
		html2canvas(document.querySelector('#capture')!).then((canvas) => {
			let a = document.createElement('a');
			a.href = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream'); // here is the most important part because if you dont replace you will get a DOM 18 exception.
			a.download = slugify(card.name) + '-card.png';

			document.body.appendChild(a);
			a.click();
		});
		sentCardToAPI();
	}

	async function sentCardToAPI() {
		if (mode == 'create') {
			$api.createCard(card);
		} else if (mode == 'update') {
			if (!cardId) {
				alert('Kartu nelze ');
				return;
			}
			$api.updateCard(card, cardId);
		}
	}

	function pf_filter(text: string) {
		// TODO: přefiltruj text a naházej symoboly/bold text tam kam patří
		return text;
	}

	let cssClass: CardTypeClass;
	const cardType = cardTypes.find((cardType) => {
		cardType.id == card.card_type_id;
	})!.name;
	$: cssClass = cardTypeClass[cardType as CardTypeKey];
</script>

<div class="{cssClass} card" id="capture">
	<section class="card-header">
		<div class="card-name">{card.name}</div>
		<div class="card-set">
			{#if cardType == 'Magický předmět' || cardType == 'Volný aspekt'}
				<div class="card-in-set">{card.in_set ? card.set_name : ''}</div>
			{/if}
		</div>
		<div class="card-type">{cardType}</div>
		{#if cardType == 'Magický předmět'}
			<div class="irremovable">
				{card.tags.includes({ name: 'Neodložitelný' }) ? 'Neodložitelný' : ''}
			</div>
		{/if}
	</section>

	<div class="card-body">
		<section class="card-content">
			<div class="card-fluff">
				{@html pf_filter(DOMPurify.sanitize(card.fluff || ''))}
			</div>
			<div class="card-effect">
				{@html pf_filter(DOMPurify.sanitize(card.effect || ''))}
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
