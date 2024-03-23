<script lang="ts">
    import type { Preset } from "../interfaces/Preset.interface";

    export let preset: Preset;
</script>

{#if preset}
    <div class="card preset-card">
        <div class="card-top">
            <div class="card-title">{preset.id}</div>
            <div class="card-subtitle">{preset.description}</div>
        </div>
        <div class="card-bottom">
            <div class="card-tag">download_path: {preset.download_path}</div>
            <div class="card-tag">media_path: {preset.media_path}</div>
            <div class="card-tag">format: {preset.format}</div>
            <div class="card-tag">template: {preset.template}</div>
            <div class="card-tag">squareCover: {preset.squareCover}</div>
            <div class="card-tag">addThumbnail: {preset.addThumbnail}</div>
            <div class="card-tag">addMetadata: {preset.addMetadata}</div>
            <div class="card-tag">addSubtitles: {preset.addSubtitles}</div>
        </div>
    </div>
{/if}

<style>
    .preset-card {
        @apply border rounded;
    }
</style>
