from fastapi import FastAPI

from app.api.media import router as media_router


app = FastAPI(
    title="Media Downloader API",
    version="0.1.0",
)


app.include_router(media_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}