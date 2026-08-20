from fastapi import APIRouter, HTTPException

from app.schemas.media import MediaInfoRequest, MediaInfoResponse
from app.services.media_service import (
    MediaExtractionError,
    get_media_info,
)


router = APIRouter(
    prefix="/api/media",
    tags=["Media"],
)


@router.post("/info", response_model=MediaInfoResponse)
def get_info(request: MediaInfoRequest):
    try:
        return get_media_info(str(request.url))

    except MediaExtractionError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )