from pydantic import BaseModel, HttpUrl


class MediaInfoRequest(BaseModel):
    url: HttpUrl


class MediaFormatResponse(BaseModel):
    format_id: str
    type: str
    quality: str
    ext: str | None
    width: int | None
    height: int | None
    fps: float | None
    filesize: int | None
    has_audio: bool


class MediaInfoResponse(BaseModel):
    title: str | None
    platform: str | None
    duration: float | None
    thumbnail: str | None
    uploader: str | None
    formats: list[MediaFormatResponse]