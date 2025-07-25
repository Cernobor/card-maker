<script lang="ts">
	export let checked: boolean = false;
	export let disabled: boolean = false;
	export let onChange: (checked: boolean) => void = () => {};
	export let id: string | undefined = undefined

	function handleChange(event: Event) {
		const input = event.target as HTMLInputElement;
		onChange(input.checked);
	}
</script>

<label class="custom-checkbox-wrapper">
	<input
		type="checkbox"
		class="custom-checkbox"
		checked={checked}
		disabled={disabled}
		on:change={handleChange}
		{id}
	/>
	<span class="custom-checkbox-ui" aria-hidden="true"></span>
</label>

<style>
.custom-checkbox-wrapper {
	position: relative;
	display: inline-block;
	width: 25px;
	height: 25px;
	cursor: pointer;
}

.custom-checkbox {
	opacity: 0;
	width: 0;
	height: 0;
	position: absolute;
}

.custom-checkbox-ui {
	display: inline-block;
	width: 100%;
	height: 100%;
	border: 2px solid #00adb5;
	border-radius: 4px;
	background-color: #1f1f1f;
	transition: all 0.5s ease;
}

.custom-checkbox:checked + .custom-checkbox-ui {
	background-color: #00adb5;
}

.custom-checkbox:checked + .custom-checkbox-ui::after {
	content: "✔";
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -60%);
	color: #1f1f1f;
	font-size: 16px;
}
</style>
