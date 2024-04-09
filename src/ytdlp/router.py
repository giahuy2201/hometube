from fastapi import APIRouter, HTTPException, Query
import starlette.status as status

from ytdlp.downloader import YTdlp
import medias.schemas as medias_schemas


router = APIRouter()


@router.get("/", response_model=list[medias_schemas.Media])
def query_medias(term: str = Query(None)):
    medias: list[medias_schemas.Media] = []
    if term.startswith("id:"):
        media_id = None
        media_id = term.split("id:")[1].strip()
        ytdlp = YTdlp(f"https://youtu.be/{media_id}")
        newMedia = ytdlp.get_media()
        if not newMedia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Failed to add media with media_id: {media_id}",
            )
        medias.append(newMedia)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Searching with non-id term is currently not supported",
        )
    return medias
