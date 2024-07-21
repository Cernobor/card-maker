<script lang="ts">
    import type { UserCreate } from "$lib/interfaces";
    let user: UserCreate;
    let passwordConfirm: string;


    function wrongRegistration(e, alertText: string) {
        e.prevendDefalt()
        user.username = "";
        user.password = "";
        passwordConfirm = "";
        alert(alertText)
    }

    function handleSubmit(e) {
        if (user.password != passwordConfirm) {
            wrongRegistration(e, "Heslo se musí shodovat!")
        }
        try {
            /*
             * TODO: saveUserOrError
             */
        } catch {
            wrongRegistration(e, `Uživatel ${user.username} už existuje.`)
        }
    }

</script>

<div>
    <form on:submit={handleSubmit}>
        <label for="username">Uživatelské jméno</label>
        <input type="text" bind:value={user.username}/>
        <label for="password">Heslo</label>
        <input type="hidden" bind:value={user.password} />
        <label for="passwordConfirm">Potvrdit heslo</label>
        <input type="hidden" bind:value={passwordConfirm} />
        <input type="submit" value="Registrovat se" />
    </form>
</div>