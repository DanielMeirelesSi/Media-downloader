from app.services.media_service import _extract_formats


def test_extract_formats_groups_video_formats_by_resolution():
    formats = _extract_formats(
        {
            "formats": [
                {
                    "format_id": "720-webm",
                    "vcodec": "vp9",
                    "acodec": "none",
                    "width": 1280,
                    "height": 720,
                    "fps": 30,
                    "ext": "webm",
                },
                {
                    "format_id": "720-mp4",
                    "vcodec": "h264",
                    "acodec": "none",
                    "width": 1280,
                    "height": 720,
                    "fps": 30,
                    "ext": "mp4",
                },
                {
                    "format_id": "480-mp4",
                    "vcodec": "h264",
                    "acodec": "none",
                    "width": 854,
                    "height": 480,
                    "fps": 30,
                    "ext": "mp4",
                },
            ],
        }
    )

    video_formats = [
        media_format
        for media_format in formats
        if media_format["type"] == "video"
    ]

    assert [media_format["quality"] for media_format in video_formats] == [
        "720p",
        "480p",
    ]


def test_extract_formats_prefers_mp4_for_equivalent_video_options():
    formats = _extract_formats(
        {
            "formats": [
                {
                    "format_id": "1080-webm",
                    "vcodec": "vp9",
                    "acodec": "none",
                    "width": 1920,
                    "height": 1080,
                    "fps": 30,
                    "ext": "webm",
                },
                {
                    "format_id": "1080-mp4",
                    "vcodec": "h264",
                    "acodec": "none",
                    "width": 1920,
                    "height": 1080,
                    "fps": 30,
                    "ext": "mp4",
                },
            ],
        }
    )

    assert formats[0]["format_id"] == "1080-mp4"
    assert formats[0]["ext"] == "mp4"


def test_extract_formats_identifies_video_audio_availability():
    formats = _extract_formats(
        {
            "formats": [
                {
                    "format_id": "720-video-audio",
                    "vcodec": "h264",
                    "acodec": "aac",
                    "width": 1280,
                    "height": 720,
                    "fps": 30,
                    "ext": "mp4",
                },
                {
                    "format_id": "1080-video-only",
                    "vcodec": "h264",
                    "acodec": "none",
                    "width": 1920,
                    "height": 1080,
                    "fps": 30,
                    "ext": "mp4",
                },
            ],
        }
    )

    by_format_id = {
        media_format["format_id"]: media_format
        for media_format in formats
    }

    assert by_format_id["720-video-audio"]["has_audio"] is True
    assert by_format_id["1080-video-only"]["has_audio"] is False


def test_extract_formats_selects_best_audio_and_represents_it_as_mp3():
    formats = _extract_formats(
        {
            "formats": [
                {
                    "format_id": "audio-low",
                    "vcodec": "none",
                    "acodec": "opus",
                    "abr": 128,
                    "ext": "webm",
                    "filesize": 1000,
                },
                {
                    "format_id": "audio-high",
                    "vcodec": "none",
                    "acodec": "mp4a.40.2",
                    "abr": 256,
                    "ext": "m4a",
                    "filesize": 2000,
                },
            ],
        }
    )

    assert formats == [
        {
            "format_id": "audio-high",
            "type": "audio",
            "quality": "256 kbps",
            "ext": "mp3",
            "width": None,
            "height": None,
            "fps": None,
            "filesize": 2000,
            "has_audio": True,
        },
    ]
