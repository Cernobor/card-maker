<script lang="ts">
	import { Color, type ColorType } from '$lib/interfaces';

	export let message: string;
	export let color: ColorType = Color.green;
	export let isDisplayed = true;
</script>

<div class="pop-up" style={`background-color: ${color}`}>
	<p class="text">
		{message}
	</p>
	<button class="close-message" on:click={() => (isDisplayed = false)}> ❌ </button>
</div>

<style>
	.pop-up {
		width: 80vw;
		border-radius: 15px;
		padding: 1px 50px;
		position: relative;
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
