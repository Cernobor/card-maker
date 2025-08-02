<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { type FlashMessage } from '$lib/interfaces';

	export let message: FlashMessage;

	const dispatch = createEventDispatcher();
</script>

<div class="pop-up" style={`background-color: ${message.color}`}>
	<p class="text">
		{message.message}
	</p>
	<button class="close-message" on:click={() => dispatch('close')}> ✖️ </button>
</div>

<style>
	.pop-up {
		width: 100%;
		border-radius: 15px;
		padding: 1px 50px;
		position: relative;
		margin: 0 20px;
	}

	.close-message {
		border: none;
		background-color: transparent;
		position: absolute;
		right: 20px;
		top: 50%;
		transform: translateY(-50%);
	}

    .text {
        font-weight: bold;
    }

	.close-message:hover {
		background-color: transparent;
	}
</style>
