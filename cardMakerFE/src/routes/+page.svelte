<script>
    
    import Card from './Card.svelte';
    //import logo from "$lib.assets/images/cb_logo_white.png";
    let curent_card = {
        name: 'Card Name',
        type: 'Card Type',
        fluff: 'Card Fluff',
        effect: 'Card Effect',
        tags:[]
    }
    let cardComponent;

</script>

<div class="body">
    <div class="header">
        <h1>Card <img src="/images/cb_logo_black.png"  width="50px"/> maker</h1>
        <nav>
            <a href="#">Home</a>
            <a href="#">vytvoř kartu</a>
            <a href="#">databáze karet</a>
            <p>Uživatel XY</p>
        </nav>

    </div>
    <div class="inputs">
        <form class = "form">
            <input type="text" placeholder="Name" bind:value={curent_card.name} />
            <input type="text" placeholder="Type" bind:value={curent_card.type} />
            <textarea bind:value={curent_card.fluff} placeholder="Fluff"></textarea>
            <textarea bind:value={curent_card.effect} placeholder="Fluff"></textarea>
        </form>
        
    </div>
    <div class="card-view">
        <Card bind:card={curent_card} bind:this={cardComponent}/>
    </div>

    <button on:click={cardComponent.saveCard}>Save</button>
</div>


<style>

    .header {
        text-align: center;
    }



</style>