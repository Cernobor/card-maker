<script lang="ts">
	import { goto } from '$app/navigation';
	import type { UserLogin } from '$lib/interfaces';
	import { api } from '$lib/stores/store';

	if ($api.loggedIn) {
		goto('/');
	}

	let user: UserLogin = {
		username: '',
		password: ''
	};

	function wrongRegistration(alertText: string) {
		user.username = '';
		user.password = '';
		alert(alertText);
	}

	async function handleSubmit(event: Event) {
		$api
			.logIn(user)
			.then(() => {
				goto('/');
			})
			.catch(() => {
				wrongRegistration('Nespravne uzivatelske jmeno nebo heslo');
			});
	}
</script>

<div class="login-form">
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
			<input type="submit" value="Prihlasit se" class="submit-button" />
		</div>
	</form>
	<div class="login-form-item">
		<p>Nemas jeste ucet? <a href="/registration">Registruj se</a>.</p>
	</div>
</div>
