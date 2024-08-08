<script>
    import { closeModal, closeAllModals, openModal, modals } from 'svelte-modals'
    import { api } from '$lib/stores/store';
	import { goto } from '$app/navigation';
      
    export let isOpen;
    export let cardName
    export let cardId
    let errorMessage = '';
	let confirmationName = '';

    function handleDelete() {
		if (confirmationName === cardName) {
			$api
				.deleteCard(cardId)
				.then(() => {

					closeAllModals();
                    goto('/card/list')
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
  <div
      role="dialog"
      class="flex overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 pointer-events-none justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"
  >
      <div class="relative p-4 w-full max-w-2xl max-h-full pointer-events-auto">
          <div
              class="relative p-4 rounded-lg shadow bg-gray-300 text-black dark:bg-gray-800 dark:text-gray-100"
          >
              <div class="flex flex-row justify-between mb-2">
                  <h2 class="flex-none text-xl">Smazat kartu</h2>
                  <button on:click={closeModal} class="flex-none">
                      <svg
                          class="w-3 h-3"
                          aria-hidden="true"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 14 14"
                      >
                          <path
                              stroke="currentColor"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                          />
                      </svg>
                      <span class="sr-only">Close modal</span></button
                  >
              </div>
              {#if errorMessage !== ''}
                  <p class="w-fit mx-auto mb-2 px-4 py-2 rounded text-center bg-red-800 text-gray-100">
                      {errorMessage}
                  </p>
              {/if}
              <div>
                  <p>
                      Určitě chcete smazat kartu <strong>{cardName}</strong>? To confirm type or copy
                      and paste name into the following field:
                  </p>
                  <input type="text" class="text-black" bind:value={confirmationName} />
                  <button class="bg-red-700 text-white px-2 py-1 rounded-lg" on:click={handleDelete}
                      >Delete</button
                  >
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
  
      /* allow click-through to backdrop */
      pointer-events: none;
    }
  
    .contents {
      min-width: 240px;
      border-radius: 6px;
      padding: 16px;
      background: white;
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