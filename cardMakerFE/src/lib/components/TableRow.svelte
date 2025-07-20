<script lang="ts">
	import type { UserPublic, CardType, CardGet } from '$lib/interfaces';

	export let card: CardGet;
	export let users: UserPublic[];
	export let types: CardType[];
	export let selectedCards: CardGet[];

	let cardAuthor: string = 'waiting...';
	let cardType: string = 'waiting...';

	async function getUserNameByID(id: number) {
		return users.filter((user) => user.id == id)[0];
	}

	async function getTypeNameByID(id: number) {
		return types.filter((type) => type.id == id)[0];
	}

	$: if (users.length) {
		(async () => {
			const response = await getUserNameByID(card.user_id || 0);
			cardAuthor = response.username;
		})();
	}
	$: if (types.length) {
		(async () => {
			const response = await getTypeNameByID(card.card_type_id);
			cardType = response.name;
		})();
	}

	let selected = false;

	function handleCheckboxChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.checked) {
			if (!selectedCards.some(c => c.id == card.id)) {
				selectedCards = [...selectedCards, card];
				selected = true;
			}
		} else {
			selectedCards = selectedCards.filter(c => c.id != card.id);
			selected = false;
		}
	}

	function updateCheckbox(selectedCards: CardGet[]) {
		if (selected && !selectedCards.includes(card) || !selected && selectedCards.includes(card)) {
			selected = !selected;
		}
	}

	$: updateCheckbox(selectedCards);
</script>

<tr>
	<td class="checkbox-column">
		<input
			class="checkbox"
			type="checkbox"
			on:change={(e) => handleCheckboxChange(e)}
			checked={selected}
		/>
	</td>
	<td><a href="/card/{card.id}"><b>{card.name}</b></a></td>
	<td>{cardAuthor}</td>
	<td>{cardType}</td>
</tr>
