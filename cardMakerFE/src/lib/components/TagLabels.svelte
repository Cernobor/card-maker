<script lang="ts">
	import type { Tag } from '$lib/interfaces';

	export let activeLabels: Tag[];
</script>

<div class="labels">
	<ul class="labels">
		{#each activeLabels as label}
			<div class="tag-label">
				<li>
					{label.name}
					<button
						class="tag-label-button"
						on:click={() => {
							activeLabels = activeLabels.filter((activeLabel) => {
								return activeLabel.name !== label.name;
							});
						}}>✖️</button
					>
				</li>
			</div>
		{/each}
	</ul>
</div>
