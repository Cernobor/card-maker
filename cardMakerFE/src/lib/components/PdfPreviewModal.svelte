<script lang="ts">
	export let blobUrl: string | null = null;
	export let open: boolean = false;
	export let onClose: () => void = () => {};
</script>

{#if open && blobUrl}
	<div class="modal-overlay" on:click={onClose}>
		<div class="modal-content" on:click|stopPropagation>
            <div class="buttons">
                <button class="modal-button" on:click={onClose}>❌</button>
            </div>
			<iframe src={blobUrl} style="width: 100%; height: 80vh; border: none;" />
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
</style>
