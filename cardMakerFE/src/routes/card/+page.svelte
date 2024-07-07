<script>
	import Card from '$lib/Card.svelte';
	import CardForm from '$lib/CardForm.svelte';
	let cardTypes = ['Magický předmět', 'Volný aspekt', 'Lokace'];


	let card = {
		name: 'Card Name',
		type: cardTypes[0],
		fluff: 'Card Fluff',
		effect: 'Efekt/pravidla karty',
		nonRemovable: true,
		in_set: false,
		set_name: 'Jméno setu (počet itemů v setu)',

		tags: []
	};
	let cardComponent;
</script>

<div class="cardmaker-body">
	<div class="inputs">
		<CardForm bind:card bind:cardTypes />
	</div>

	<div class="card-view">
		<Card bind:card bind:this={cardComponent} />
		<button on:click={cardComponent.saveCard} style="width:80px; height:30px">Save</button>
	</div>
</div>

<style>
	.card-view {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 20px;
	}
</style>
