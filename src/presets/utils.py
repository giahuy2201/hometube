import medias.schemas as medias_schemas
import presets.schemas as presets_schemas
from yt_dlp.utils import sanitize_filename


def get_media_path(preset: presets_schemas.Preset, media: medias_schemas.Media):
    return f"{preset.media_path}/{media.uploader}/{media.title}"


def infer_file_name(preset: presets_schemas.Preset, media: medias_schemas.Media):
    file_ext = "flac" if preset.squareCover else "mkv"
    # Title in info.json and media file name could be different since yt-dlp replace chars like *:<>?|/\\ with their respective full width versions to avoid filename problems on different fs
    return sanitize_filename(  # mimic the way yt-dlp sanitize file names
        preset.template
        % {
            "title": media.title,
            "id": media.id,
            "ext": file_ext,
        }
    )
