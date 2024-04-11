<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import type { Task } from "../../interfaces/Task.interface";
  import ChannelCard from "../../components/ChannelCard.svelte";

  const tasks = writable<Task[]>([]);

  const fetchTasks = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/daemon/");
      const data = await response.json();
      tasks.set(data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  onMount(fetchTasks);
</script>

<h1>Tasks</h1>

<table class="table-fixed w-full">
  <thead>
    <tr>
      <th>ID</th>
      <th>Priority</th>
      <th>Type</th>
      <th>Status</th>
      <th>When</th>
      <th>After #</th>
      <th>Media Title</th>
      <th>Preset Format</th>
    </tr>
  </thead>
  <tbody>
    {#each $tasks as task}
      <tr>
        <td class="task-item">{task.id}</td>
        <td class="task-item">{task.priority}</td>
        <td class="task-item">{task.type}</td>
        <td class="task-item">{task.status}</td>
        <td class="task-item">{task.when}</td>
        <td class="task-item">{task.after}</td>
        <td class="task-item">{task.media.title}</td>
        <td class="task-item">{task.preset.format}</td>
      </tr>
    {/each}
  </tbody>
</table>
