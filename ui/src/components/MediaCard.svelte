<script lang="ts">
  import type { Media } from "../interfaces/Media.interface";

  export let media: Media;
</script>

{#if media}
  <a class="card media-card" href="/medias/{media.id}">
    <div class="card-top">
      <div class="card-image">
        <img src={media.thumbnail} alt={media.uploader_id} />
      </div>
      <div class="card-overlay"><div>{media.duration}s</div></div>
    </div>
    <div class="card-bottom">
      <div class="card-title">{media.title}</div>
      <div class="card-subtitle">{media.uploader} - {media.upload_date}</div>
    </div>
  </a>
{/if}
