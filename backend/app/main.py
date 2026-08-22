import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.media import router as media_router


DEFAULT_CORS_ORIGINS = "http://localhost:5173"


def get_cors_origins() -> list[str]:
    origins = os.environ.get("CORS_ORIGINS") or DEFAULT_CORS_ORIGINS

    return [
        origin.strip()
        for origin in origins.split(",")
        if origin.strip()
    ]


app = FastAPI(
    title="Media Downloader API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


app.include_router(media_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
