<script lang="ts">
	import { goto } from '$app/navigation';
	import HTTPError from '$lib/errors';
	import type { UserCreate, FlashMessage } from '$lib/interfaces';
	import { Color } from '$lib/interfaces';
	import { api } from '$lib/stores/store';
	import { PUBLIC_USE_API_KEY } from '$env/static/public';
	import PopUpMessage from '$lib/components/PopUpMessage.svelte';
	import { fade } from 'svelte/transition';

	let user: UserCreate = {
		username: '',
		password: '',
		api_key: ''
	};
	let passwordConfirm: string = '';

	let flashMessages: FlashMessage[] = [];
	$: flashMessages;

	function pushFlash(message: string, color = Color.red) {
		const item = { message, color, id: Date.now() + Math.random() };
		flashMessages = [...flashMessages, item];
		setTimeout(() => {
			flashMessages = flashMessages.filter((m) => m.id !== item.id);
		}, 4000);
	}

	function wrongRegistration(msg: string) {
		user.username = '';
		user.password = '';
		passwordConfirm = '';
		pushFlash(msg, Color.red);
	}

	async function handleSubmit(event: Event) {
		event.preventDefault();
		user.username = user.username.trim();

		if ([...user.username].length < 4) {
			wrongRegistration('❌ Uživatelské jméno musí mít alespoň 4 znaky.');
			return;
		}

		if ([...user.username].length > 20) {
			wrongRegistration('❌ Uživatelské jméno nemůže být delší než 20 znaků.');
			return;
		}

		if (user.password !== passwordConfirm) {
			wrongRegistration('❌ Hesla se musí shodovat!');
			return;
		}

		try {
			await $api.createUser(user);
			goto('/login?created=true');
		} catch (error) {
			if (error instanceof HTTPError) {
				if (error.code === 401) {
					wrongRegistration('❌ Zadaný tajný klíč je nesprávný!');
				} else if (error.code === 403) {
					wrongRegistration(
						`❌ Uživatel ${user.username} už existuje, zvol si jiné uživatelské jméno.`
					);
				} else {
					wrongRegistration('❌ Registrace se nezdařila.');
				}
			} else {
				wrongRegistration('❌ Registrace se nezdařila.');
			}
		}
	}
</script>

<div class="content">
	<!-- Flash messages -->
	<div class="flash-message-wrapper">
		{#each flashMessages as message (message.id)}
			<div class="pop-up-wrapper" in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
				<PopUpMessage
					{message}
					on:close={() => {
						flashMessages = flashMessages.filter((m) => m !== message);
					}}
				/>
			</div>
		{/each}
	</div>

	<div class="cardmaker-body-wrapper">
		<div class="cardmaker-body">
			<div class="login-form box">
				<form on:submit={handleSubmit} class="login-form">
					<div class="login-form-item">
						<label for="username">Uživatelské jméno *</label>
						<input
							type="text"
							bind:value={user.username}
							on:blur={() => (user.username = user.username.trim())}
							class="login-form-input"
							required
						/>
					</div>
					<div class="login-form-item">
						<label for="password">Heslo</label>
						<input type="password" bind:value={user.password} class="login-form-input" />
					</div>
					<div class="login-form-item">
						<label for="passwordConfirm">Potvrdit heslo</label>
						<input type="password" bind:value={passwordConfirm} class="login-form-input" />
					</div>
					{#if PUBLIC_USE_API_KEY === 'true'}
						<div class="login-form-item">
							<label for="api-key">Tajný klíč</label>
							<input type="text" bind:value={user.api_key} required class="login-form-input" />
						</div>
					{/if}
					<input type="submit" value="Registrovat se" class="submit-button" />
				</form>
				<div class="login-form-item">
					<p>Máš už účet? <a href="/login">Přihlaš se</a>.</p>
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	.pop-up-wrapper {
		justify-content: center;
		display: flex;
		margin-top: 15px;
	}
	.flash-message-wrapper {
		display: block;
		width: 100%;
	}
</style>
