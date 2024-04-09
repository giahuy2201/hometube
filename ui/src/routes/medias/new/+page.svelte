<script lang="ts">
    import { writable } from "svelte/store";
    import type { Media } from "../../../interfaces/Media.interface";
    import MediaCard from "../../../components/MediaCard.svelte";

    export let term = "";

    const foundMedias = writable<Media[]>();

    const searchMedia = async (term: string) => {
        try {
            const response = await fetch(
                "http://localhost:8000/api/ytdlp/?term=" + term,
            );
            const data = await response.json();
            foundMedias.set(data);
        } catch (error) {
            console.error("Error search medias:", error);
        }
    };
    function handleKeyPress(event: { key: string }) {
        if (event.key === "Enter") {
            searchMedia(term);
        }
    }
</script>

<div class="relative text-gray-600 m-4">
    <input
        type="search"
        class="w-full py-2 pl-4 pr-4 rounded-lg border border-gray-300 focus:outline-none focus:border-indigo-500"
        placeholder="eg. id:####"
        bind:value={term}
        on:keydown={handleKeyPress}
    />
</div>

{#if $foundMedias}
    <ul class="">
        {#each $foundMedias as media}
            <li>
                <MediaCard {media} fullWidth />
            </li>
        {/each}
    </ul>
{/if}

<style>
</style>
