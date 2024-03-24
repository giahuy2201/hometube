<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { page } from "$app/stores";
  import type { Media } from "../../../interfaces/Media.interface";
  import MediaCard from "../../../components/MediaCard.svelte";
  import type { Channel } from "../../../interfaces/Channel.interface";
  import ChannelCard from "../../../components/ChannelCard.svelte";

  const channel = writable<Channel>();
  const medias = writable<Media[]>([]);

  const fetchChannel = async () => {
    try {
      let id = $page.params.id;
      const response = await fetch("http://localhost:8000/api/channels/" + id);
      const data = await response.json();
      channel.set(data);
    } catch (error) {
      console.error("Error fetching channel:", error);
    }
  };

  const fetchMedias = async () => {
    try {
      let channel_id = $page.params.id;
      const response = await fetch(
        "http://localhost:8000/api/medias?channel_id=" + channel_id,
      );
      const data = await response.json();
      medias.set(data);
    } catch (error) {
      console.error("Error fetching medias:", error);
    }
  };

  onMount(() => {
    fetchMedias();
    fetchChannel();
  });
</script>

<div class="w-2/12">
  <ChannelCard channel={$channel} />
</div>

<h2>Media</h2>

<ul
  class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-2"
>
  {#each $medias as media}
    <li>
      <MediaCard {media} />
    </li>
  {/each}
</ul>
