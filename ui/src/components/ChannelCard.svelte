<script lang="ts">
  import type { Channel } from "../interfaces/Channel.interface";

  export let channel: Channel;
</script>

{#if channel}
  <a class="card channel-card" href="/channels/{channel.channel_id}">
    <div class="card-top">
      <div class="card-image">
        <img src={channel.thumbnail} alt={channel.uploader_id} />
      </div>
    </div>
    <div class="card-bottom">
      <div class="card-title">{channel.channel}</div>
      <div class="card-subtitle">{channel.channel_follower_count} subs</div>
    </div>
  </a>
{/if}
