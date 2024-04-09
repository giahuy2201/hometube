<script lang="ts">
    export let placeholder = "Search...";
    export let value = "";
    export let onInput = () => {};
</script>

<div class="relative text-gray-600 m-4">
    <input
        type="search"
        class="w-full py-2 pl-4 pr-4 rounded-lg border border-gray-300 focus:outline-none focus:border-indigo-500"
        {placeholder}
        {value}
        on:input={onInput}
    />
</div>

<style>
</style>
