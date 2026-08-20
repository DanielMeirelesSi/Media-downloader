from pydantic import BaseModel, HttpUrl


class MediaInfoRequest(BaseModel):
    url: HttpUrl
    

class MediaInfoResponse(BaseModel):
    title: str | None
    platform: str | None
    duration: float | None
    thumbnail: str | None
    uploader: str | None