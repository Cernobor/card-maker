<script>
	import { closeModal, closeAllModals, openModal, modals } from 'svelte-modals';
	import { api } from '$lib/stores/store';
	import { goto } from '$app/navigation';

	export let isOpen;
	export let cardName;
	export let cardId;
	let errorMessage = '';
	let confirmationName = '';

	function handleDelete() {
		if (confirmationName === cardName) {
			$api
				.deleteCard(cardId)
				.then(() => {
					closeAllModals();
					goto('/card/list');
				})
				.catch((error) => {
					errorMessage = error.message;
				});
		} else {
			errorMessage = 'Confirmation name does not match card name';
		}
	}
</script>

{#if isOpen}
	<div role="dialog" class="modal">
		<div class="modal-contents">
			<div class="modal-header">
				<div class="modal-close-button">
					<button on:click={closeModal} class="close-modal">X</button>
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
                        Určitě chcete smazat kartu <strong>{cardName}</strong>? Pro potvrzení napište název karty.
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
		background: rgba(193, 192, 183, 0.33);
	}

	.modal-contents {
		min-width: 140px;
		padding: 16px;
		background-color: #31363f;
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
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
    }
	.close-modal {
		width: 40px;
		height: 40px;
	}
    .modal-error {
        color: orangered;
    }
    .modal-confirm {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

	h2 {
		text-align: center;
		font-size: 24px;
	}

	p {
		text-align: center;
		margin-top: 16px;
	}
</style>
