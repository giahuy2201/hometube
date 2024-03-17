<script lang="ts">
	import SideBar from "./SideBar.svelte";
	import TopBar from "./TopBar.svelte";
	import "./styles.css";
</script>

<div class="app">
	<SideBar />
	<div class="main">
		<TopBar />
		<slot />
	</div>
</div>
