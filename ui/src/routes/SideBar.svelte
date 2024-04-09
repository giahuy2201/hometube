<script lang="ts">
	import { page } from "$app/stores";
	import { onMount } from "svelte";
	import "./styles.css";

	$: pathname = $page.route.id;
	$: showWatchMenu =
		pathname && (pathname == "/watch" || pathname.startsWith("/medias"));
</script>

<div class="sidebar">
	<div class="logo">HomeTube</div>
	<div class="nav">
		<a class="nav-item" href="/watch">
			<span>Logo</span> <span>Watch</span>
		</a>
		{#if showWatchMenu}
			<ul class="nav">
				<a class="nav-item" href="/medias/new">Add New Media</a>
				<a class="nav-item" href="/medias/import">Library Import</a>
			</ul>
		{/if}
		<a class="nav-item" href="/channels">
			<span>Logo</span> <span>Channels</span>
		</a>
		<a class="nav-item" href="/calendar">
			<span>Logo</span> <span>Calendar</span>
		</a>
		<a class="nav-item" href="/activity">
			<span>Logo</span> <span>Activity</span>
		</a>
		<a class="nav-item" href="/settings">
			<span>Logo</span> <span>Settings</span>
		</a>
		<a class="nav-item" href="/system">
			<span>Logo</span> <span>System</span>
		</a>
	</div>
	<div class="footer">
		<div class="support">
			<span>Logo</span> Support
		</div>
		<div class="version">
			<a href="/#">v0.1.0</a>
		</div>
	</div>
</div>
