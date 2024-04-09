<script lang="ts">
  import type { Media } from "../interfaces/Media.interface";

  export let media: Media;
  export let fullWidth: boolean = false;
</script>

{#if media}
  {#if fullWidth}
    <a class="card media-card card-full" href="/medias/{media.id}">
      <div class="card-left">
        <div class="card-image">
          <img src={media.thumbnail} alt={media.uploader_id} />
        </div>
        <div class="card-overlay"><div>{media.duration}s</div></div>
      </div>
      <div class="card-right">
        <div class="card-title">{media.title}</div>
        <div class="card-subtitle">{media.uploader} - {media.upload_date}</div>
        <div class="card-description">{media.description}</div>
      </div>
    </a>
  {:else}
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
{/if}

<style>
  .card-full {
    @apply flex;
  }
  .card-left {
    @apply w-1/5;
  }
  .card-right {
    @apply flex flex-col pl-4 w-4/5;
  }
  .card-title {
    @apply font-bold text-xl;
  }
  .card-subtitle,
  .card-extras,
  .card-description {
    @apply my-1;
  }
  .card-tag {
    @apply inline-block px-2 m-1 bg-neutral-300;
  }
  .card-description {
    /* @apply text-ellipsis overflow-hidden; */
  }
</style>
