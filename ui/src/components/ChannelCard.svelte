<script lang="ts">
  import type { Channel } from "../interfaces/Channel.interface";

  export let channel: Channel;
</script>

<div class="card channel-card">
  <div class="card-top">
    <div class="card-image">
      <img src={channel.thumbnail} alt={channel.uploader_id} />
    </div>
  </div>
  <div class="card-bottom">
    <div class="card-title">{channel.channel}</div>
    <div class="card-subtitle">{channel.channel_follower_count}</div>
  </div>
</div>
