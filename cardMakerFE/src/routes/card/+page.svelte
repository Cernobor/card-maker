<script>
	import Card from '$lib/Card.svelte';
	import CardForm from '$lib/CardForm.svelte';
	let cardTypes = ['Magický předmět', 'Volný aspekt', 'Lokace'];

	//import logo from "$lib.assets/images/cb_logo_white.png";
	
	let card = {
		name: 'Card Name',
		type: cardTypes[0],
		fluff: 'Card Fluff',
		effect: 'Efekt/pravidla karty',
		nonRemovable: true,
		inSet: false,
		setName: 'Jméno setu (počet itemů v setu)',

		tags: []
	};
	let cardComponent;

</script>

<div class="cardmaker-body">
	<div class="inputs">
		<CardForm bind:card bind:cardTypes/>
	</div>

	<div class="card-view">
		<Card bind:card bind:this={cardComponent} />
		<button on:click={cardComponent.saveCard} style="width:80px; height:30px">Save</button>
	</div>
</div>

<style>
	textarea {
		width: 400px;
		height: 100px;
	}
	.card-view {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 20px;
	}
</style>
