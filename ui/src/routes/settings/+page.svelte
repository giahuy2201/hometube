<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import type { Preset } from "../../interfaces/Preset.interface";
  import PresetCard from "../../components/PresetCard.svelte";

  const presets = writable<Preset[]>([]);

  const fetchPresets = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/presets/");
      const data = await response.json();
      presets.set(data);
    } catch (error) {
      console.error("Error fetching presets:", error);
    }
  };

  onMount(fetchPresets);
</script>

<h1>Presets</h1>

<ul>
  {#each $presets as preset}
    <li>
      <PresetCard {preset} />
    </li>
  {/each}
</ul>
