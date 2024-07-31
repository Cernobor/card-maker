<script lang="ts">
	import { goto } from '$app/navigation';
	import HTTPError from '$lib/errors';
	import type { UserCreate } from '$lib/interfaces';
	import { api } from '$lib/stores/store';

	let user: UserCreate = {
		username: '',
		password: '',
		api_key: ''
	};
	let passwordConfirm: string = '';

	function wrongRegistration(alertText: string) {
		user.username = '';
		user.password = '';
		passwordConfirm = '';
		alert(alertText);
	}

	async function handleSubmit(event: Event) {
		if (user.password != passwordConfirm) {
			event.preventDefault();
			wrongRegistration('Hesla se musí shodovat!');
		}
		$api
			.createUser(user)
			.then(() => {
				goto('/login');
			})
			.catch((error) => {
				if (error instanceof HTTPError) {
					if (error.code === 401) {
						wrongRegistration('Zadaný tajný klíč je nesprávný!');
					} else if (error.code === 403) {
						wrongRegistration(
							`Uživatel ${user.username} už existuje, zvol si jiné uživatelské jméno.`
						);
					} else {
						wrongRegistration('Registrace se nezdařila.');
					}
				} else {
					wrongRegistration('Registrace se nezdařila.');
				}
			});
	}
</script>

<div class="cardmaker-body">
	<form on:submit={handleSubmit} class="login-form">
		<div class="login-form-item">
			<label for="username">Uživatelské jméno</label>
			<input type="text" bind:value={user.username} class="login-form-input" required />
		</div>
		<div class="login-form-item">
			<label for="password">Heslo</label>
			<input type="password" bind:value={user.password} class="login-form-input" />
		</div>
		<div class="login-form-item">
			<label for="passwordConfirm">Potvrdit heslo</label>
			<input type="password" bind:value={passwordConfirm} class="login-form-input" />
		</div>
		<div class="login-form-item">
			<label for="api-key">Tajný klíč</label>
			<input type="text" bind:value={user.api_key} required class="login-form-input" />
		</div>
		<input type="submit" value="Registrovat se" class="submit-button" />
	</form>
</div>
