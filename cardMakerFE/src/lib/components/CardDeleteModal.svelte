<script lang="ts">
	import { closeModal, closeAllModals, openModal, modals } from 'svelte-modals';
	import { api } from '$lib/stores/store';
	import { goto } from '$app/navigation';

	export let isOpen;
	export let cardName;
	export let cardId: number;
	let errorMessage = '';
	let confirmationName = '';

	function handleDelete() {
		console.log("entered handleDelete")
		if (confirmationName === "smazat") {
			console.log("after smazat")
			$api
				.deleteCard(cardId)
				.then(() => {
					console.log("after delete")
					closeAllModals();
					goto('/card/list');
				})
				.catch((error) => {
					errorMessage = error.message;
				});
		} else {
			errorMessage = 'Pro potvrzení napište "smazat"';
		}
	}
</script>

{#if isOpen}
	<div role="dialog" class="modal">
		<div class="modal-contents">
			<div class="modal-header">
				<div class="modal-close-button">
					<button class="cancel-button close-modal" on:click={closeModal} >❌</button>
				</div>
				<div class="modal-title">
					<h2 style="margin-top:0px">Smazat kartu</h2>
				</div>
			</div>
            <div class="modal-body">
			{#if errorMessage !== ''}
				<p class="modal-error">
					{errorMessage}
				</p>
			{/if}
                <div class="modal-confirm">
                    <p>
                        Určitě chcete smazat kartu <strong>{cardName}</strong>? Pro potvrzení napište <b><i>"smazat"</i></b>.
                    </p>
                    <div>
                    <input type="text" class="text-black" style ="margin-right:15px;" bind:value={confirmationName} />
                    <button on:click={handleDelete}>Potvrdit smazání</button
                    >
                    </div>
                </div>
            </div>
		</div>
	</div>
{/if}

<style>
	.modal {
		position: fixed;
		top: 0;
		bottom: 0;
		right: 0;
		left: 0;
		display: flex;
		justify-content: center;
		align-items: center;
		background: rgba(0, 0, 0, 0.7);
		z-index: 9999;
	}

	.modal-contents {
		min-width: 140px;
		padding: 30px;
		background-color: #161a20;
		color: #eeeeee;
		border-radius: 20px;
		border-color: #00adb5;
		border-style: outset;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		pointer-events: auto;
	}
	.modal-header {
		display: flex;
		flex-direction: column;
	}
    .modal-close-button {
		position: relative;
    }
	.close-modal {
		width: 40px;
		height: 40px;
		position: absolute;
		top: -20px;
		right: -20px;
	}
    .modal-error {
        color: orangered;
    }
    .modal-confirm {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

	p {
		text-align: center;
		margin: 10px;
		margin-bottom: 15px;
	}
	
	.modal-title {
		text-align: center;
		font-size: 24px;
		font-family: 'Inknut Antiqua', serif;
		line-height: 100%;
	}
</style>
