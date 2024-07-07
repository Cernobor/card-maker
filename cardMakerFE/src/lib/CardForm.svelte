<script>
	export let card;
	let cardTypeProp = card.type;
	export let cardTypes;

	$: {
		card.type = cardTypeProp;
		if (cardTypeProp == 'Magický předmět') {
			card.inSet = false;
			card.setName = 'Jméno setu (počet itemů v setu)';
		} else if (cardTypeProp == 'Volný aspekt') {
			card.inSet = false;
			card.setName = 'Jméno rodiny aspektů';
		}
	}
</script>

<div class="inputs">
	<form class="card-input-form">
		<label for="name">Jméno:</label>

		<input type="text" placeholder="Name" id="name" bind:value={card.name} />
		<label for="type">Typ:</label>
		<select bind:value={cardTypeProp}>
			{#each cardTypes as type (type)}
				<option value={type}>{type}</option>
			{/each}
		</select>

		<label for="fluff">Fluff:</label>

		<textarea bind:value={card.fluff} placeholder="fluff" id="fluff" />
		<label for="efect">Efekt/pravidla:</label>
		<textarea bind:value={card.effect} placeholder="efekt" id="efect" />

		{#if card.type == 'Magický předmět'}
			<label for="nonremovable">Neodložitelný:</label>
			<input type="checkbox" bind:checked={card.nonRemovable} id="nonremovable" />

			<label for="inSet">V setu:</label>
			<input type="checkbox" bind:checked={card.inSet} id="inSet" />
			{#if card.inSet}
				<label for="setName">Jméno setu:</label>
				<input type="text" bind:value={card.setName} id="setName" />
			{/if}
		{/if}

		{#if card.type == 'Volný aspekt'}
			<label for="aspectFamily">V rodině apektů:</label>
			<input type="checkbox" bind:checked={card.inSet} id="aspectFamily" />
			{#if card.inSet}
				<label for="aspectFamilyName">Jméno rodiny aspektů:</label>
				<input type="text" bind:value={card.setName} id="aspectFamilyName" />
			{/if}
		{/if}
	</form>
</div>

<style>
	textarea {
		width: 400px;
		height: 100px;
	}
</style>
