from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.media import router as media_router


app = FastAPI(
    title="Media Downloader API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(media_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}