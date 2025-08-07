<script lang="ts">
	import { goto } from '$app/navigation';
	import type { UserLogin, FlashMessage, ColorType } from '$lib/interfaces';
	import { Color } from '$lib/interfaces';
	import { api } from '$lib/stores/store';
	import PopUpMessage from '$lib/components/PopUpMessage.svelte';
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	export let data: { userCreated: boolean };

	if ($api.loggedIn) {
		goto('/');
	}

	let user: UserLogin = {
		username: '',
		password: ''
	};

	let flashMessages: FlashMessage[] = [];
	$: flashMessages;

	function pushFlash(message: string, color: ColorType = Color.red) {
		const item = { message, color, id: Date.now() + Math.random() };
		flashMessages = [...flashMessages, item];
		// Auto-dismiss after 4s
		setTimeout(() => {
			flashMessages = flashMessages.filter((m) => m.id !== item.id);
		}, 4000);
	}

	function wrongLogin(msg: string) {
		user.username = '';
		user.password = '';
		pushFlash(msg, Color.red);
	}

	onMount(() => {
		if (data?.userCreated) {
			pushFlash('✅ Registrace proběhla úspěšně. Teď se přihlaš.', Color.green);
			// clear the query param so refresh won’t re-trigger the flash
			goto('/login', { replaceState: true, noScroll: true });
		}
	});

	async function handleSubmit(event: Event) {
		event.preventDefault();
		$api
			.logIn(user)
			.then(() => {
				goto('/');
			})
			.catch(() => {
				wrongLogin('❌ Nesprávné uživatelské jméno nebo heslo!');
			});
	}
</script>

<div class="content">
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
						<input type="text" bind:value={user.username} class="login-form-input" required />
					</div>
					<div class="login-form-item">
						<label for="password">Heslo</label>
						<input type="password" bind:value={user.password} class="login-form-input" />
					</div>
					<div class="login-form-item">
						<input type="submit" value="Přihlásit se" class="submit-button" />
					</div>
				</form>
				<div class="login-form-item">
					<p>Nemáš ještě účet? <a href="/registration">Registruj se</a>.</p>
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
