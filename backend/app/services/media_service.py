import yt_dlp
from yt_dlp.utils import DownloadError


class MediaExtractionError(Exception):
    pass


def _extract_formats(info: dict) -> list[dict]:
    formats = []
    seen_formats = set()

    for media_format in info.get("formats") or []:
        format_id = media_format.get("format_id")

        if not format_id:
            continue

        video_codec = media_format.get("vcodec")
        audio_codec = media_format.get("acodec")

        has_video = video_codec not in (None, "none")
        has_audio = audio_codec not in (None, "none")

        if not has_video and not has_audio:
            continue

        width = media_format.get("width")
        height = media_format.get("height")
        fps = media_format.get("fps")
        extension = media_format.get("ext")

        filesize = (
            media_format.get("filesize")
            or media_format.get("filesize_approx")
        )

        if has_video:
            media_type = "video"

            if height:
                quality = f"{height}p"
            else:
                quality = media_format.get("format_note") or "video"

        else:
            media_type = "audio"
            bitrate = media_format.get("abr")

            if bitrate:
                quality = f"{round(bitrate)} kbps"
            else:
                quality = "audio"

        format_key = (
            quality,
            extension,
            has_video,
            has_audio,
        )

        if format_key in seen_formats:
            continue

        seen_formats.add(format_key)

        formats.append(
            {
                "format_id": str(format_id),
                "type": media_type,
                "quality": quality,
                "ext": extension,
                "width": width,
                "height": height,
                "fps": fps,
                "filesize": filesize,
                "has_audio": has_audio,
            }
        )

    formats.sort(
        key=lambda item: (
            item["type"] == "audio",
            -(item["height"] or 0),
        )
    )

    return formats


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
        "formats": _extract_formats(info),
    }