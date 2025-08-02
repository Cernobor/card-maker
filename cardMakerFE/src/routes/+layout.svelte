<script lang="ts">
	import { page } from '$app/stores';
	import './styles.css';
	import { Modals, closeAllModals } from 'svelte-modals';
	import { goto } from '$app/navigation';
	import UserIcon from '$lib/components/UserIcon.svelte';
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" />

<div class="header-block">
	<div class="header-content">
		<div class="left-logo">
			<h1 class="page-title">
				Card <img alt="CB logo" src="/images/cb_logo_white.png" width="45px" /> Maker
			</h1>
		</div>

		<nav class="navbar">
			<a class={$page.url.pathname === '/' ? 'active-tab' : ''} href="/">ℹ️ Info</a>
			<a class={$page.url.pathname === '/card' ? 'active-tab' : ''} href="/card">📄 Nová karta</a>
			<a class={$page.url.pathname === '/card/list' ? 'active-tab' : ''} href="/card/list"
				>🗂️ Seznam karet</a
			>
		</nav>

		<UserIcon />
	</div>
</div>

<div class="content-container">
		<slot class="content" />
	<Modals>
		<div
			slot="backdrop"
			class="fixed top-0 bottom-0 right-0 left-0 bg-black/50"
			on:click={closeAllModals}
		></div>
	</Modals>
</div>
<div>
	<footer class="footer-block">
		<p class="footer-text">Černobor Cardmaker</p>
	</footer>
</div>

<style>
	.header-block {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 8vh;
		background-color: #161a20;
		border-bottom: #00adb5 inset;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 999;
	}

	.header-content {
		position: relative; /* důležité pro absolutní pozicování nav */
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 20px;
	}

	.left-logo .page-title {
		font-size: 26px;
		margin: 0;
		display: flex;
		align-items: center;
		gap: 10px;
		font-family: 'Inknut Antiqua', serif;
	}

	.navbar {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		display: flex;
		gap: 10px;
	}

	.navbar a {
		padding: 6px 18px;
		background-color: #161a20;
		text-decoration: none;
		color: #eeeeee;
		border-radius: 8px;
		transition: background-color 0.2s;
		font-weight: 500;
		font-size: 16px;
		font-family: 'Inknut Antiqua', serif;
	}

	.navbar a:hover:not(.active-tab) {
		background-color: #1f232a;
	}

	.active-tab {
		background-color: #24282e;
		box-shadow: inset 0 0 0 2px #00adb5;
	}

	.page-title {
		margin-top: 0;
		font-size: 32px;
		padding-bottom: 0;
		margin-bottom: 0;
	}

	.content-container {
		margin: 0;
		margin-top: 8vh;
		padding: 0;
		min-height: 85.5vh;
		position: relative;
		display: flex;
	}

	.footer-block {
		position: relative;
		left: 0;
		bottom: 0;
		width: 100%;
		height: 6vh;
		background-color: #161a20;
		font-family: 'Montserrat', sans-serif;
		font-size: 14px;
		color: #eeeeee;
		text-align: center;
		margin: 0;
		border-top: #00adb5 outset;

		display: flex;
		align-items: center;
		justify-content: center;
	}

	.footer-text {
		display: inline-block;
		vertical-align: middle;
		font-family: 'Inknut Antiqua', serif;
		padding: 0;
	}

	.left-logo {
		display: flex;
		align-items: center;
		justify-content: flex-start;
		flex: 1;
	}
</style>
