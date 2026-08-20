import yt_dlp


def get_media_info(url: str):
    ydl_options = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "platform": info.get("extractor_key"),
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail"),
        "uploader": info.get("uploader"),
    }