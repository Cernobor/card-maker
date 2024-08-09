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
            <div class="flex flex-row justify-between mb-2">
                <h2 class="flex-none text-xl">Smazat kartu</h2>
                <button on:click={closeModal} class="flex-none">
                    X
                    </button
                >
            </div>
            {#if errorMessage !== ''}
                <p class="w-fit mx-auto mb-2 px-4 py-2 rounded text-center bg-red-800 text-gray-100">
                    {errorMessage}
                </p>
            {/if}
            <div>
                <p>
                    Určitě chcete smazat kartu <strong>{cardName}</strong>? To confirm type or copy and paste
                    name into the following field:
                </p>
                <input type="text" class="text-black" bind:value={confirmationName} />
                <button class="bg-red-700 text-white px-2 py-1 rounded-lg" on:click={handleDelete}
                    >Delete</button
                >
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
        background: rgba(193, 192, 183, 0.33)  
	}

	.modal-contents {
		min-width: 240px;
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

	h2 {
		text-align: center;
		font-size: 24px;
	}

	p {
		text-align: center;
		margin-top: 16px;
	}

	.actions {
		margin-top: 32px;
		display: flex;
		justify-content: space-between;
		gap: 8px;
	}
</style>
