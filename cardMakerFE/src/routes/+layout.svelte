<script>
    import './styles.css';
</script>


<div class="header-block">
    <h1>Card <img src="/images/cb_logo_black.png"  width="50px"/> maker</h1>
    <nav>
        <a href="#">Home</a>
        <a href="#">vytvoř kartu</a>
        <a href="#">databáze karet</a>
        <p>Uživatel XY</p>
    </nav>
</div>


<slot/>

<style>
    
    .header-block{  /* not working no idea why, also nothing in styles.css */
    font-family: "Montserrat-Regular"; 
    font-weight: bold;
    src: local("fonts/Montserrat/Montserrat-Regular.ttf") format("truetype");
}
</style>