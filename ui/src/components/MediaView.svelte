<script lang="ts">
    // Add TypeScript code for Videos page
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import type { Media } from "../interfaces/Media.interface";
    import MediaCard from "./MediaCard.svelte";

    // Initialize store for videos data
    const medias: Media[] = writable([]);

    // Fetch medias data on component mount
    onMount(async () => {
        const response = await fetch("localhost:8000/api/medias");
        const data = await response.json();
        medias.set(data);
    });
</script>

<div
    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
>
    <!-- Video Card -->

    {#each medias as media}
        <div class="bg-white rounded shadow p-4">
            <MediaCard {media} />
        </div>
    {/each}
    <!-- Repeat video card markup for other videos -->
</div>
