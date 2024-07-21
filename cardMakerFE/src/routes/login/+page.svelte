<script lang="ts">
    import type { UserCreate } from "$lib/interfaces";
    import { Cookies } from "js-cookie";
    let user: UserCreate;

    function handleSubmit(e) {
        try {
            /*
             * TODO: getTokenOrError
             */
            let JWTToken = "";
            Cookies.set("token", JWTToken);
        } catch {
            e.prevendDefalt()
            user.username = "";
            user.password = "";
            alert("Nesprávné uživatelské jméno nebo heslo.")
        }
    }

</script>

<div>
    <form on:submit={handleSubmit}>
        <label for="username">Uživatelské jméno</label>
        <input type="text" bind:value={user.username}/>
        <label for="password">Heslo</label>
        <input type="hidden" bind:value={user.password} />
        <input type="submit" value="Přihlásit se" />
    </form>
</div>