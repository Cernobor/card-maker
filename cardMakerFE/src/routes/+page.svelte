<script>
	import HelpText from '$lib/components/HelpText.svelte';
</script>

<h1 class="center">Vítejte na Černobor CardMakeru!</h1>
<div class="home-page">
	<div class="home-page-item">
		<h1>Úvod</h1>
		<p>
			Zde si můžete vytvářet kartičky <b>Lokací</b>,
			<b>Magických předmětů</b> a <b>Volných aspektů</b>.
		</p>
		<p>
			Pro vytváření karet je <b>potřeba být přihlášený</b>. Při registraci je vyžadován tajný klíč,
			o ten si požádejte.
		</p>
		<p>
			Karty můžete upravovat i mazat, ale dávejte pozor, jestli nemažete někomu jeho kartu, asi by
			vás za to neměl moc rád.
		</p>
	</div>
	<div class="home-page-item">
		<h1>Formátování</h1>
		<HelpText />
	</div>
	<div class="home-page-item">
		<h1>Tagy a filtry</h1>
		<p>
			Ka každé kartě můžete přidávat tagy, podle kterých je dále možné karty filtrovat. Každá karta
			dostane po vytoření <b>tag roku</b>, kdy byla vytvořena.
		</p>
		<p>
			Filtrovat můžete také podle <b>Autora karty</b> a <b>typu karty</b>.
		</p>
		<p>
			Můžete přidávat i vlastní tagy. Pozor na to, že se nový tag
			<b>uloží až poté, co ho přidáte ke kartě</b> a tu uložíte do databáze!
		</p>
	</div>
</div>
