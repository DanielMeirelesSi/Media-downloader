import yt_dlp
from yt_dlp.utils import DownloadError


class MediaExtractionError(Exception):
    pass


def get_media_info(url: str):
    ydl_options = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)

    except DownloadError as error:
        message = str(error).lower()

        if "login" in message or "cookies" in message:
            raise MediaExtractionError(
                "This media may require authentication."
            )

        if "private" in message:
            raise MediaExtractionError(
                "This media is private or unavailable."
            )

        if "unsupported url" in message:
            raise MediaExtractionError(
                "This URL is not supported."
            )

        raise MediaExtractionError(
            "Unable to extract media information."
        )

    return {
        "title": info.get("title"),
        "platform": info.get("extractor_key"),
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail"),
        "uploader": info.get("uploader"),
    }