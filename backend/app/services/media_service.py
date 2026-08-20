import shutil
import tempfile
from pathlib import Path

import yt_dlp
from yt_dlp.utils import DownloadError


class MediaExtractionError(Exception):
    pass


def _extract_formats(info: dict) -> list[dict]:
    video_formats = {}
    audio_formats = []

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
            dimensions = [
                value
                for value in (width, height)
                if isinstance(value, (int, float)) and value > 0
            ]

            resolution = int(min(dimensions)) if len(dimensions) == 2 else 0

            if resolution:
                quality = f"{resolution}p"
            else:
                quality = media_format.get("format_note") or "Vídeo"

            candidate = {
                "format_id": str(format_id),
                "type": "video",
                "quality": quality,
                "ext": extension,
                "width": width,
                "height": height,
                "fps": fps,
                "filesize": filesize,
                "has_audio": has_audio,
                "_resolution": resolution,
            }

            existing = video_formats.get(quality)

            def score(item):
                return (
                    item["ext"] == "mp4",
                    item["has_audio"],
                    item["fps"] or 0,
                )

            if existing is None or score(candidate) > score(existing):
                video_formats[quality] = candidate

        else:
            audio_formats.append(
                {
                    "format_id": str(format_id),
                    "type": "audio",
                    "quality": (
                        f"{round(media_format.get('abr'))} kbps"
                        if media_format.get("abr")
                        else "Áudio"
                    ),
                    "ext": extension,
                    "width": None,
                    "height": None,
                    "fps": None,
                    "filesize": filesize,
                    "has_audio": True,
                    "_bitrate": media_format.get("abr") or 0,
                }
            )

    videos = sorted(
        video_formats.values(),
        key=lambda item: item["_resolution"],
        reverse=True,
    )

    result = []

    for video in videos:
        video.pop("_resolution", None)
        result.append(video)

    if audio_formats:
        best_audio = max(
            audio_formats,
            key=lambda item: item["_bitrate"],
        )

        best_audio.pop("_bitrate", None)
        result.append(best_audio)

    return result


def download_media(url: str, format_id: str):
    temp_dir = Path(tempfile.mkdtemp(prefix="media-downloader-"))

    try:
        info_options = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(info_options) as ydl:
            info = ydl.extract_info(url, download=False)

        selected_format = next(
            (
                media_format
                for media_format in info.get("formats") or []
                if str(media_format.get("format_id")) == format_id
            ),
            None,
        )

        if selected_format is None:
            raise MediaExtractionError(
                "Selected format is not available."
            )

        has_video = selected_format.get("vcodec") not in (None, "none")
        has_audio = selected_format.get("acodec") not in (None, "none")

        if has_video and not has_audio:
            format_selector = f"{format_id}+bestaudio/best"
        else:
            format_selector = format_id

        download_options = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "format": format_selector,
            "outtmpl": str(temp_dir / "media.%(ext)s"),
            "merge_output_format": "mp4",
        }

        with yt_dlp.YoutubeDL(download_options) as ydl:
            downloaded_info = ydl.extract_info(url, download=True)

        files = [
            file
            for file in temp_dir.iterdir()
            if file.is_file()
            and file.suffix not in {".part", ".ytdl"}
        ]

        if not files:
            raise MediaExtractionError(
                "The media file could not be created."
            )

        file_path = max(
            files,
            key=lambda file: file.stat().st_mtime,
        )

        title = downloaded_info.get("title") or "media"
        safe_title = "".join(
            char
            for char in title
            if char not in '<>:"/\\|?*'
        ).strip()

        if not safe_title:
            safe_title = "media"

        download_name = f"{safe_title}{file_path.suffix}"

        return file_path, download_name, temp_dir

    except DownloadError as error:
        shutil.rmtree(temp_dir, ignore_errors=True)

        message = str(error).lower()

        if "requested format is not available" in message:
            raise MediaExtractionError(
                "Selected format is no longer available."
            )

        if "login" in message or "cookies" in message:
            raise MediaExtractionError(
                "This media may require authentication."
            )

        raise MediaExtractionError(
            "Unable to download this media."
        )

    except MediaExtractionError:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


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