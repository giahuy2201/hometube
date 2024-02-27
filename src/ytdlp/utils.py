from presets.schemas import Preset


def getParams(preset: Preset):
    """
    Convert preset to yt-dlp compatible params
    """
    params = {}
    params["verbose"] = False
    # file naming and format
    params["format"] = preset.format
    params["outtmpl"] = preset.template
    # output location
    paths = {}
    paths["home"] = preset.download_path
    params["paths"] = paths
    # write non-video data too
    params["writeinfojson"] = True
    params["writesubtitles"] = True
    params["writethumbnail"] = True
    # postprocessors, order matters
    postprocessors = []
    # audio stuff & media container
    if preset.squareCover:
        postprocessors.append(
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "flac",
                "preferredquality": 0,
                "nopostoverwrites": True,
            }
        )
    else:
        # postprocessors.append(
        #         {
        #             "key": "FFmpegVideoRemuxer",
        #             "preferedformat": "mkv",
        #         }
        # )
        params["merge_output_format"] = "mkv"
    # embed info into media file
    if preset.addMetadata:
        postprocessors.append(
            {
                "key": "FFmpegMetadata",
                "add_chapters": True,
                "add_metadata": True,
                "add_infojson": not preset.squareCover,  # info-json can only be attached to mkv/mka files
            }
        )
    # TODO: Add custom postprocessor to cut square thumbnails for audio
    if preset.addThumbnail:
        postprocessors.append(
            {
                "key": "FFmpegThumbnailsConvertor",
                "format": "jpg",
                "when": "before_dl",
            }
        )
        postprocessors.append(
            {
                "key": "SquareCover",
            }
        )
        postprocessors.append(
            {
                "key": "EmbedThumbnail",
                "already_have_thumbnail": True,
            }
        )
    if preset.addSubtitles:
        postprocessors.append(
            {"key": "FFmpegEmbedSubtitle", "already_have_subtitle": True}
        )
    params["postprocessors"] = postprocessors
    # hooks
    progress_hooks = []

    return params
