<script lang="ts">
	import { PUBLIC_BASE_API_URL } from '$env/static/public';
	import { slugify } from '$lib/slugify.ts';
	import html2canvas from 'html2canvas';
	import DOMPurify from 'isomorphic-dompurify';
	export let mode = 'create';

	interface Card {
		name: string;
		type: string;
		fluff: string;
		effect: string;
		nonRemovable: boolean;
		in_set: boolean;
		setName: string;
		tags: string[];
	}

	let cardTypeClass: string;

	export let card: Card = {};



	async function getCardTypes() {
		const url = PUBLIC_BASE_API_URL + '/cardmaker/card-types';
		try {
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}

			const json = await response.json();
			return json;
		} catch (error) {
			console.error(error.message);
		}
	}

	export function saveCard() {
		html2canvas(document.querySelector('#capture')).then((canvas) => {
			let a = document.createElement('a');
			a.href = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream'); // here is the most important part because if you dont replace you will get a DOM 18 exception.
			a.download = slugify(card.name) + '-card.png';

			document.body.appendChild(a);
			a.click();
		});
		sentCardToAPI();
	}

	async function sentCardToAPI() {
		let cardTypes = await getCardTypes();
		let cardTypeId = cardTypes.find((typeElement) => typeElement.name == card.type).id;
		let requestMethod, url, requestBody;
		console.log('CARD', card);

		if (mode == 'create') {
			requestMethod = 'POST';
			url = PUBLIC_BASE_API_URL + '/cardmaker/cards';
			requestBody = {
				name: card.name,
				fluff: card.fluff,
				effect: card.effect,
				user_id: 1, // TODO: get user id from session
				card_type_id: cardTypeId,
				in_set: card.in_set,
				set_name: card.setName,
				tags: card.tags
			};
		} else if (mode == 'update') {
			requestMethod = 'PUT';
			url = PUBLIC_BASE_API_URL + '/cardmaker/cards/' + card.id;
			requestBody = {
				id: card.id,
				name: card.name,
				fluff: card.fluff,
				effect: card.effect,
				user_id: 1, // TODO: get user id from session
				card_type_id: 1,
				in_set: card.in_set,
				set_name: card.set_name,
				tags: card.tags
			};
			console.log('TOTO SE POSÍLÁ');
			console.log(requestBody);
		}

		try {
			const response = await fetch(url, {
				method: requestMethod,
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(requestBody)
			});
			console.log(response);
			if (!response.ok) {
				alert(
					'Něco se pokazilo, karta se neuložila do databáze, po odkliknutí tohoto okna si jí ale stále můžete alespoň stáhnout'
				);
				throw new Error(`Response status: ${response.status}`);
			}

			const json = await response.json();
			console.log(json);
		} catch (error) {
			console.error(error.message);
		}
	}

	function pf_filter(text) {
		// TODO: přefiltruj text a naházej symoboly/bold text tam kam patří
		return text;
	}

	$: if (card.type == 'Magický předmět') {
		cardTypeClass = 'card-magical-item';
	} else if (card.type == 'Volný aspekt') {
		cardTypeClass = 'card-free-aspect';
	} else if (card.type == 'Lokace') {
		cardTypeClass = 'card-location';
	}
</script>

<div class="{cardTypeClass} card" id="capture">
	<section class="card-header">
		<div class="card-name">{card.name}</div>
		<div class="card-set">
			{#if card.type == 'Magický předmět'}
				<div class="card-in-set">{card.in_set ? card.setName : ''}</div>
			{:else if card.type == 'Volný aspekt'}
				<div class="card-in-set">{card.in_set ? card.setName : ''}</div>
			{/if}
		</div>
		<div class="card-type">{card.type}</div>
		{#if card.type == 'Magický předmět'}
			<div class="irremovable">{card.nonRemovable ? 'Neodložitelný' : ''}</div>
		{/if}
	</section>

	<div class="card-body">
		<section class="card-content">
			<div class="card-fluff">
				{@html pf_filter(DOMPurify.sanitize(card.fluff))}
			</div>
			<div class="card-effect">
				{@html pf_filter(DOMPurify.sanitize(card.effect))}
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
