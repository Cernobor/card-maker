<script lang="ts">
	import type { UserPublic, CardType, CardGet } from '$lib/interfaces';

	export let card: CardGet;
	export let users: UserPublic[];
	export let types: CardType[];

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
</script>

<tr>
	<td><a href="/card/{card.id}"><b>{card.name}</b></a></td>
	<td>{cardAuthor}</td>
	<td>{cardType}</td>
</tr>
