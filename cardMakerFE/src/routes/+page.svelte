<script>
    import Card from './Card.svelte';
    //import logo from "$lib.assets/images/cb_logo_white.png";
    let card = {
        name: 'Card Name',
        type: 'Card Type',
        fluff: 'Card Fluff',
        effect: 'Card Effect'
    }
</script>

<div class="body">
    <div class="header">
        <h1>Card <img src="/images/cb_logo_black.png"  width="50px"/> maker</h1>
    </div>
    <div class="inputs">

        <input type="text" placeholder="Name" bind:value={card.name} />
        <input type="text" placeholder="Type" bind:value={card.type} />
        <textarea bind:value={card.fluff} placeholder="Fluff"></textarea>
        <textarea bind:value={card.effect} placeholder="Fluff"></textarea>
        

    </div>
    <div class="card-view"><Card /></div>
</div>


<style>
    @media print {
        @page {
        margin: 7mm;
        }
        .header, .inputs {
        display: none;
        }
    }
    .header {
        text-align: center;
    }



</style>