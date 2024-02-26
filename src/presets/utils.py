import medias.schemas as medias_schemas
import presets.schemas as presets_schemas


def get_media_path(preset: presets_schemas.Preset, media: medias_schemas.Media):
    return f"{preset.media_path}/{media.uploader}/{media.title}"


def infer_file_name(preset: presets_schemas.Preset, media: medias_schemas.Media):
    file_ext = "flac" if preset.squareCover else "mkv"
    return preset.template % {
        "title": media.title,
        "id": media.id,
        "ext": file_ext,
    }
