<script lang="ts">
	import "./styles.css";
</script>

<div class="topbar">
    <!-- Search Box -->
    <div class="search">
        <!-- Search Box Input (Visible on Medium and Larger Screens) -->
        <input
            type="text"
            placeholder="Search"
            class="sm:block w-full p-2 rounded-md bg-gray-800 text-white focus:outline-none"
        />
    </div>

    <!-- Notification and Avatar Buttons -->
    <div class="actions flex items-center space-x-4">
        <button class="notifs text-white">Notification</button>
        <button class="user text-white">Avatar</button>
    </div>
</div>
