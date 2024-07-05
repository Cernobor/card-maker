<script>
    import html2canvas from 'html2canvas';
    import Card from './Card.svelte';
    //import logo from "$lib.assets/images/cb_logo_white.png";
    let curent_card = {
        name: 'Card Name',
        type: 'Card Type',
        fluff: 'Card Fluff',
        effect: 'Card Effect',
        tags:[]
    }

    function saveCard(){
        html2canvas(document.querySelector("#capture")).then(canvas => {
            var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");  // here is the most important part because if you dont replace you will get a DOM 18 exception.
            window.location.href=image;     
        });
    }
</script>

<div class="body">
    <div class="header">
        <h1>Card <img src="/images/cb_logo_black.png"  width="50px"/> maker</h1>
    </div>
    <div class="inputs">

        <input type="text" placeholder="Name" bind:value={curent_card.name} />
        <input type="text" placeholder="Type" bind:value={curent_card.type} />
        <textarea bind:value={curent_card.fluff} placeholder="Fluff"></textarea>
        <textarea bind:value={curent_card.effect} placeholder="Fluff"></textarea>
        
    </div>
    <div class="card-view">
        <Card bind:card={curent_card}/>
    </div>

    <button on:click={saveCard}>Save</button>
</div>


<style>

    .header {
        text-align: center;
    }



</style>