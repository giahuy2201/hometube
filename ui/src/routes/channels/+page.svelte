<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import type { Channel } from "../../interfaces/Channel.interface";
  import ChannelCard from "../../components/ChannelCard.svelte";

  const channels = writable<Channel[]>([]);

  const fetchChannels = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/channels/");
      const data = await response.json();
      channels.set(data);
    } catch (error) {
      console.error("Error fetching channels:", error);
    }
  };

  onMount(fetchChannels);
</script>

<h1>Followed Channels</h1>

<ul
  class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-2"
>
  {#each $channels as channel}
    <li>
      <ChannelCard {channel} />
    </li>
  {/each}
</ul>
