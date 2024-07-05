<script lang="ts">
	import html2canvas from 'html2canvas';
	import DOMPurify from 'isomorphic-dompurify';

  let cardTypeClass:string
	export let card = {
	};

	function slugify(str) {
		return String(str)
			.normalize('NFKD') // split accented characters into their base characters and diacritical marks
			.replace(/[\u0300-\u036f]/g, '') // remove all the accents, which happen to be all in the \u03xx UNICODE block.
			.trim() // trim leading or trailing whitespace
			.toLowerCase() // convert to lowercase
			.replace(/[^a-z0-9 -]/g, '') // remove non-alphanumeric characters
			.replace(/\s+/g, '-') // replace spaces with hyphens
			.replace(/-+/g, '-'); // remove consecutive hyphens
	}


	export function saveCard() {
		html2canvas(document.querySelector('#capture')).then((canvas) => {
			let a = document.createElement('a');
			a.href = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream'); // here is the most important part because if you dont replace you will get a DOM 18 exception.
			a.download = slugify(card.name) + '-card.png';

			document.body.appendChild(a);
			a.click();
		});
	}

	function pf_filter(text) {
		// TODO: přefiltruj text a naházej symoboly/bold text tam kam patří
		return text;
	}
  $: if (card.type == 'Magický předmět') {
  cardTypeClass = 'card-magical-item' 
  } else if (card.type == 'Volný aspekt') {
    cardTypeClass = 'card-free-aspect'
  } else if (card.type == 'Lokace') {
    cardTypeClass = 'card-location'
  }
</script>

<div class="{cardTypeClass} card" id="capture">
  <section class="card-header">
		<div class="card-name">{card.name}</div>
		<div class="card-type">{card.type}</div>
    {#if card.type == 'Magický předmět'}
    <div class="irremovable">{card.nonRemovable ? 'Neodložitelný' : ""}</div>



    {/if}
	</section>



	<section class="content">
		<div class="card-fluff">
			{@html pf_filter(DOMPurify.sanitize(card.fluff))}
		</div>
		<div class="card-effect">
			{@html pf_filter(DOMPurify.sanitize(card.effect))}
		</div>
	</section>
  <section clas="card-set">
  {#if card.type == 'Magický předmět'}
  <div class="card-in-set">{card.inSet ? card.setName : ""}</div>
  {:else if card.type == 'Volný aspekt'}
  <div class="card-in-set">{card.inAspectFamily ? card.aspectFamilyName : ""}</div>
  {/if}
  </section>
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
		padding: 0 4pt;
	}
	.card-name{
		font-family: "Inknut Antiqua", serif;
		font-size: 10pt;
		font-weight: bold;
    text-transform: capitalize;
	}
	.card-type {
		font-family: "Montserrat", sans-serif;
		font-size: 10pt;
		font-weight: 8;
	}

	.content {
		margin-top: 1pt;
	}
	.content div {
		padding: 0 4pt;
	}
	:global(section.content p) {
		padding-bottom: 2pt;
		margin: 0;
	}
	.description {
		border-top: 1pt solid black;
		text-align: justify;
	}
	:global(img.activity) {
		max-height: 8pt;
	}
	.description :global(img :not(.activity)) {
		display: block;
		margin: auto;
	}
</style>
