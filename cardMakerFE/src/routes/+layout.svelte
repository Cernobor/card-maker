<script>
	import './styles.css';
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
	href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
	rel="stylesheet"
/>

<div class="header-block">
	<h1>Card <img src="/images/cb_logo_black.png" width="50px" /> maker</h1>
	<nav class="navbar">
		<a href="#">Home</a>
		<a href="#">vytvoř kartu</a>
		<a href="#">databáze karet</a>
		<p>Uživatel XY</p>
	</nav>
</div>

<slot />
