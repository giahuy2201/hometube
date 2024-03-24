<script lang="ts">
  import type { Channel } from "../interfaces/Channel.interface";

  export let channel: Channel;
</script>

{#if channel}
  <div class="banner channel-banner">
    <div class="banner-left">
      <div class="banner-image">
        <img src={channel.thumbnail} alt={channel.uploader_id} />
      </div>
    </div>
    <div class="banner-right">
      <div class="banner-title">{channel.channel}</div>
      <div class="banner-subtitle">
        {channel.uploader_id} - {channel.channel_follower_count} subscribers
      </div>
      <div class="banner-extras">
        <div class="banner-tag">media_path/{channel.uploader}</div>
        <div class="banner-tag">size</div>
        <div class="banner-tag">{channel.uploader_id}</div>
      </div>
      <div class="banner-description">{channel.description}</div>
    </div>
  </div>
{/if}

<style>
  .banner-left {
    @apply w-1/5;
  }
  .banner-right {
    @apply flex flex-col pl-4 w-4/5;
  }
  .banner-title {
    @apply font-bold text-xl;
  }
  .banner-subtitle,
  .banner-extras,
  .banner-description {
    @apply my-1;
  }
  .banner-tag {
    @apply inline-block px-2 m-1 bg-neutral-300;
  }
</style>
