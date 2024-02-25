import medias.schemas as medias_schemas
import presets.schemas as presets_schemas


def infer_path(preset: presets_schemas.Preset, media: medias_schemas.Media):
    file_ext = "m4a" if preset.squareCover else "mkv"
    file_name = preset.template % {
        "title": media.title,
        "id": media.id,
        "ext": file_ext,
    }
    return f"{preset.destination}/{file_name}"
