<script lang="ts">
    export let errorMessage: String = "404: Not found";
</script>

<div class="error-page">
    <h1>{errorMessage}</h1>
</div>

<style>
    .error-page {
        background-color: #222831;
        padding: 20px;
        margin: 10% 25%;
        color: #ff7f50;
        border-radius: 20px;
        border-color: #00adb5;
        justify-items: center;
    }
</style>