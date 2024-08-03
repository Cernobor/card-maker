<script lang="ts">
	import './styles.css';
	import { api } from '$lib/stores/store';
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" />

<div class="header-block">
	<h1 class="page-title">
		Card <img alt="CB logo" src="/images/cb_logo_white.png" width="45px" /> Maker
	</h1>
	<nav class="navbar">
		<a href="/">Domů</a>
		<a href="/card">Vytvoř kartu</a>
		<a href="/card/list">Databáze karet</a>
		{#if $api.loggedIn}
			<a href="/logout">Odhlásit se</a>
		{:else}
			<a href="/login">Přihlásit se</a>
		{/if}
	</nav>
</div>
<div class="content-container">
	<div class="main-content">
		<slot />
	</div>
</div>
<div>
	<footer class="footer-block">
		<p class="footer-text">Černobor Cardmaker</p>
	</footer>
</div>
