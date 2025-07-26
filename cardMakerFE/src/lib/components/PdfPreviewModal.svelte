<script lang="ts">
	import { tick } from 'svelte';

	export let blobUrl: string | null = null;
	export let open: boolean = false;
	export let onClose: () => void = () => {};

	let iframeRef: HTMLIFrameElement;

	$: if (open && blobUrl) {
		tick().then(() => {
			iframeRef?.focus();
		});
	}
</script>

{#if open && blobUrl}
	<div class="modal-overlay" on:click={onClose} role="presentation">
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
		<div
			class="modal-content"
			role="dialog"
			aria-modal="true"
			aria-labelledby="modal-title"
			on:click|stopPropagation
		>
			<!-- optional visible label (for screen readers) -->
			<h2 id="modal-title" class="visually-hidden">PDF Preview</h2>

			<div class="buttons">
				<button
					class="modal-button"
					on:click={onClose}
					type="button"
					aria-label="Close preview dialog"
				>
					❌
				</button>
			</div>

			<iframe
				bind:this={iframeRef}
				src={blobUrl}
				style="width: 100%; height: 80vh; border: none;"
				title="Preview of generated PDF"
				tabindex="-1"
			/>
		</div>
	</div>
{/if}

<style>
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		background: rgba(0, 0, 0, 0.7);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 999;
	}

	.modal-content {
		background: #222831;
		padding: 20px;
		border-radius: 8px;
		width: 90vw;
		max-width: 1000px;
		max-height: 90vh;
		overflow: auto;
		position: relative;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
	}

	.buttons {
		display: flex;
		flex-direction: row;
		justify-content: flex-end;
		gap: 0.5rem;
		margin: 0;
		padding: 0;
	}

	.modal-button {
		background: none;
		border: none;
		cursor: pointer;
		margin-top: 0;
		padding-top: 0;
	}

	.visually-hidden {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
	}
</style>
