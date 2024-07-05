<script lang="ts">
	import html2canvas from 'html2canvas';
	import DOMPurify from 'isomorphic-dompurify';
	export let card = {
		tags: []
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

	export let name: string,
		type,
		tags = [],
		attributes: string,
		description: string;

	export function saveCard() {
		html2canvas(document.querySelector('#capture')).then((canvas) => {
			let a = document.createElement('a');
			a.href = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream'); // here is the most important part because if you dont replace you will get a DOM 18 exception.
			a.download = slugify(card.name) + '.png';

			document.body.appendChild(a);
			a.click();
		});
	}

	function pf_filter(text) {
		// TODO: přefiltruj text a naházej symoboly/bold text tam kam patří
		return text;
	}
</script>

<div class="card" id="capture">
	<section class="card-header">
		<div class="name">{card.name}</div>
		<div class="type">{card.type}</div>
	</section>
	<section class="tags">
		{#each card.tags as tag}
			{#if tag.toLowerCase() == 'uncommon'}
				<div class="tag uncommon">{tag}</div>
			{:else if tag.toLowerCase() == 'rare'}
				<div class="tag rare">{tag}</div>
			{:else if tag.toLowerCase() == 'unique'}
				<div class="tag unique">{tag}</div>
			{:else}
				<div class="tag">{tag}</div>
			{/if}
		{/each}
	</section>
	<section class="content">
		<div class="attributes">
			{@html pf_filter(DOMPurify.sanitize(card.attributes))}
		</div>
		<div class="description">
			{@html pf_filter(DOMPurify.sanitize(card.description))}
		</div>
	</section>
</div>

<style>
	.card {
		width: calc(2.5in - 4mm);
		height: calc(3.5in - 4mm);
		font-size: 8pt;
		border: 2mm solid black;
		/*background-image: url("/bg.webp");*/
		background-clip: border-box;
		page-break-after: auto;
		page-break-inside: avoid;
	}
	.card-header {
		display: flex;
		justify-content: space-between;
		border-bottom: 2px solid black;
		padding: 0 4pt;
	}
	.name,
	.type {
		font-family: serif;
		font-size: 10pt;
		font-weight: bold;
	}
	.tags {
		padding: 1pt 4pt;
		display: flex;
		flex-wrap: wrap;
	}
	.tag {
		font-family: sans-serif;
		font-size: 6pt;
		font-variant: all-small-caps;
		color: white;
		background-color: #5e0000;
		padding: 0.5pt 1pt;
		border: 1pt solid #d9c484;
	}
	.uncommon {
		background-color: #98513d;
	}
	.rare {
		background-color: #002664;
	}
	.unique {
		background-color: #54166e;
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
