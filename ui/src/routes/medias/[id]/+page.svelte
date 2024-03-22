<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { page } from "$app/stores";
  import type { Media } from "../../../interfaces/Media.interface";
  import MediaCard from "../../../components/MediaCard.svelte";
  import type { Channel } from "../../../interfaces/Channel.interface";
  import ChannelCard from "../../../components/ChannelCard.svelte";

  const media = writable<Media>();

  const fetchMedia = async () => {
    try {
      let id = $page.params.id;
      const response = await fetch("http://localhost:8000/api/medias/" + id);
      const data = await response.json();
      media.set(data);
    } catch (error) {
      console.error("Error fetching medias:", error);
    }
  };

  onMount(fetchMedia);
</script>

<div class="w-2/12">
  <MediaCard media={$media} />
</div>

<h2>Versions</h2>

{#if $media}
  <ul
    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-2"
  >
    {#each $media.versions as version}
      <li>
        {version.id}
      </li>
    {/each}
  </ul>
{/if}
