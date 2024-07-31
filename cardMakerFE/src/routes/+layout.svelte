<script lang="ts">
	import './styles.css';
	import { api } from '$lib/stores/store';
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
	href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
	rel="stylesheet"
/>

<div class="header-block">
	<h1>Card <img alt="CB logo" src="/images/cb_logo_white.png" width="50px" /> Maker</h1>
	<nav class="navbar">
		<a href="/">Home</a>
		<a href="/card">vytvoř kartu</a>
		<a href="/card/list">databáze karet</a>
		{#if $api.loggedIn}
			<a href="/logout">Odhlásit se</a>
		{:else}
			<a href="/login">Přihlásit se</a>
		{/if}
	</nav>
</div>
<div class="page-container">
	<slot class="main-content" />
</div>
<footer class="footer-block">
	<p>Černobor Cardmaker</p>
</footer>
