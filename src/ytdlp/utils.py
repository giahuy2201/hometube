from presets.schemas import Preset


def getParams(preset: Preset):
    """
    Convert preset to yt-dlp compatible params
    """
    params = {}
    params["format"] = preset.format
    params["outtmpl"] = preset.template
    # output location
    paths = {}
    paths["home"] = preset.destination
    paths["temp"] = "./temp"
    params["paths"] = paths
    params["addmetadata"] = preset.addMetadata
    params["writethumbnail"] = preset.addThumbnail
    postprocessors = []
    # audio
    if preset.squareCover:
        params["format"] = "bestaudio"
        # Extract audio using ffmpeg
        postprocessors.append(
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            },
        )
    else:
        params["merge_output_format"] = "mkv"
    if preset.addMetadata:
        postprocessors.append(
            {
                "key": "FFmpegMetadata",
            }
        )
    params["postprocessors"] = postprocessors
    # hooks
    progress_hooks = []

    return params
