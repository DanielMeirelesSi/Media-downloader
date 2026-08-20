from pydantic import BaseModel, Field, HttpUrl


class MediaInfoRequest(BaseModel):
    url: HttpUrl


class MediaDownloadRequest(BaseModel):
    url: HttpUrl
    format_id: str = Field(min_length=1, max_length=100)


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