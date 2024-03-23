<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import type { Media } from "../../interfaces/Media.interface";
  import MediaCard from "../../components/MediaCard.svelte";

  const medias = writable<Media[]>([]);

  const fetchMedias = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/medias/");
      const data = await response.json();
      medias.set(data);
    } catch (error) {
      console.error("Error fetching medias:", error);
    }
  };

  onMount(fetchMedias);
</script>

<h1>Medias</h1>

<ul
  class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-2"
>
  {#each $medias as media}
    <li>
      <MediaCard {media} />
    </li>
  {/each}
</ul>
