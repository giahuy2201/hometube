<script lang="ts">
	import SideBar from "./SideBar.svelte";
	import TopBar from "./TopBar.svelte";
	import "./styles.css";
</script>

<div class="app">
	<SideBar />
	<div class="main">
		<TopBar />
		<div class="content">
			<slot />
		</div>
	</div>
</div>
