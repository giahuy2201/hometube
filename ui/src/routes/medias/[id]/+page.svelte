<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { page } from "$app/stores";
  import type { Media } from "../../../interfaces/Media.interface";
  import MediaCard from "../../../components/MediaCard.svelte";
  import type { Channel } from "../../../interfaces/Channel.interface";
  import ChannelCard from "../../../components/ChannelCard.svelte";
  import ChannelAvatar from "../../../components/ChannelAvatar.svelte";

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

{#if $media}
  <div class="media-player">
    <img src={$media.thumbnail} alt={$media.uploader_id} />
  </div>
  <h1 class="media-title">{$media.title}</h1>

  <ChannelAvatar channel={$media.channel} />

  <div class="media-extras">
    <div class="media-tag">{$media.upload_date}</div>
    <div class="media-tag">{$media.view_count} views</div>
    <div class="media-tag">{$media.duration}s</div>
    {#if $media.was_live}
      <div class="media-tag">LIVE</div>
    {/if}
  </div>

  <div class="media-description">{$media.description}</div>

  <h2>Versions</h2>
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

<style>
  .media-player {
    @apply m-4;
  }
  .media-player > img {
    @apply w-full rounded-md;
  }
  .media-title {
    @apply text-3xl font-semibold text-gray-900 mx-4;
  }
  .media-extras {
    @apply mx-4 mb-4;
  }
  .media-tag {
    @apply inline-block px-2 m-1 bg-neutral-300;
  }
  .media-description {
    @apply mx-4;
    white-space: pre-line; /* preserve new lines */
  }
</style>
