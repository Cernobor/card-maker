<script lang="ts">
	import { api } from '$lib/stores/store';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let userClicked = false;
	let container: HTMLDivElement | null = null;

	function handleLogin() {
		sessionStorage.setItem('loggedIn', 'true');
		goto('/login');
		userClicked = false;
	}

	function handleLogout() {
		sessionStorage.setItem('loggedIn', 'false');
		goto('/logout');
		userClicked = false;
	}

	function handleClickOutside(event: MouseEvent) {
		if (userClicked && container && !container.contains(event.target as Node)) {
			userClicked = false;
		}
	}

	onMount(() => {
		// Only runs in browser — safe to access document here
		document.addEventListener('click', handleClickOutside);
		return () => {
			// Clean up safely when component is destroyed
			document.removeEventListener('click', handleClickOutside);
		};
	});

    $: $api.loggedIn;
</script>

<div bind:this={container}>
	<div class="user-wrapper">
		{#if $api.loggedIn}
			<span>{$api.currentUser?.username}</span>
		{/if}
		<button class="user-button" on:click={() => (userClicked = !userClicked)}>
			<img src="/user-icon.svg" alt="User" />
		</button>
		{#if userClicked}
			<div class="user-dropdown">
				{#if $api.loggedIn}
					<button on:click={handleLogout}>Odhlásit se</button>
				{:else}
					<button on:click={handleLogin}>Přihlásit se</button>
				{/if}
			</div>
		{/if}
	</div>
</div>


<style>
	.user-wrapper {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.user-wrapper span {
		font-size: 16px;
		color: #eeeeee;
		font-family: 'Inknut Antiqua', serif;
	}

	.user-button {
		width: 100%;
		height: 100%;
		border-radius: 50%;
		border: 2px solid #00adb5;
		background-color: #24282e;
		cursor: pointer;
		padding: 0;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.user-button:hover {
		background-color: #161a20;
	}

	.user-button img {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		object-fit: cover;
	}

	.user-dropdown {
		position: absolute;
		top: 60px;
		right: 0;
		background-color: #161a20;
		border-radius: 5px;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
		padding: 2px;
		z-index: 1000;
		display: flex;
		flex-direction: column;
		min-width: 120px;
	}

	.user-dropdown button {
		all: unset;
		padding: 12px;
		cursor: pointer;
		border-radius: 4px;
		transition: background-color 0.2s;
	}

	.user-dropdown button:hover {
		color: #00adb5;
	}
</style>
