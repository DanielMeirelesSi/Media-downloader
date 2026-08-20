import shutil

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from app.schemas.media import (
    MediaDownloadRequest,
    MediaInfoRequest,
    MediaInfoResponse,
)
from app.services.media_service import (
    MediaExtractionError,
    download_media,
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


@router.post("/download")
def download(request: MediaDownloadRequest):
    try:
        file_path, filename, temp_dir = download_media(
            str(request.url),
            request.format_id,
        )

        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/octet-stream",
            background=BackgroundTask(
                shutil.rmtree,
                temp_dir,
                ignore_errors=True,
            ),
        )

    except MediaExtractionError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )