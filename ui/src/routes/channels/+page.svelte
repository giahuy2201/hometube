<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  const channels = writable([]);

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

<h1>List of Channels</h1>

<ul>
  {#each $channels as channel}
    <li>{channel["channel"]}</li>
  {/each}
</ul>
