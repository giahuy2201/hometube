<script lang="ts">
  import type { Channel } from "../interfaces/Channel.interface";

  export let channel: Channel;
</script>

{#if channel}
  <div class="avatar channel-avatar">
    <div class="avatar-left">
      <div class="avatar-image">
        <img src={channel.thumbnail} alt={channel.uploader_id} />
      </div>
    </div>
    <div class="avatar-middle">
      <div class="avatar-title">{channel.channel}</div>
      <div class="avatar-subtitle">
        {channel.channel_follower_count} subscribers
      </div>
    </div>
    <div class="avatar-right">
      <button class="action">Add Channel</button>
    </div>
  </div>
{/if}

<style>
  .avatar {
    @apply w-96 m-4 flex;
  }
  .avatar-left {
    @apply w-1/5;
  }
  .avatar-image > img {
    @apply block rounded-full;
  }
  .avatar-middle {
    @apply flex flex-col flex-grow pl-4 place-content-center;
  }
  .avatar-right {
    @apply flex flex-col place-content-center w-auto;
  }
  .action {
    @apply bg-red-600 hover:bg-red-700 text-white px-3 py-3 rounded-xl shadow-md;
  }
  .avatar-title {
    @apply font-semibold text-xl;
  }
  .avatar-subtitle {
    @apply my-1;
  }
</style>
