from fastapi.testclient import TestClient

from app.api import media as media_api
from app.main import app
from app.services.media_service import MediaExtractionError


def test_media_info_returns_service_response(monkeypatch):
    def fake_get_media_info(url: str):
        assert url == "https://example.com/video"

        return {
            "title": "Example video",
            "platform": "Example",
            "duration": 123.0,
            "thumbnail": "https://example.com/thumb.jpg",
            "uploader": "Example uploader",
            "formats": [
                {
                    "format_id": "video-720",
                    "type": "video",
                    "quality": "720p",
                    "ext": "mp4",
                    "width": 1280,
                    "height": 720,
                    "fps": 30,
                    "filesize": 123456,
                    "has_audio": True,
                },
            ],
        }

    monkeypatch.setattr(media_api, "get_media_info", fake_get_media_info)

    client = TestClient(app)

    response = client.post(
        "/api/media/info",
        json={"url": "https://example.com/video"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "title": "Example video",
        "platform": "Example",
        "duration": 123.0,
        "thumbnail": "https://example.com/thumb.jpg",
        "uploader": "Example uploader",
        "formats": [
            {
                "format_id": "video-720",
                "type": "video",
                "quality": "720p",
                "ext": "mp4",
                "width": 1280,
                "height": 720,
                "fps": 30.0,
                "filesize": 123456,
                "has_audio": True,
            },
        ],
    }


def test_media_info_returns_400_on_extraction_error(monkeypatch):
    def fake_get_media_info(url: str):
        raise MediaExtractionError("Unable to extract media information.")

    monkeypatch.setattr(media_api, "get_media_info", fake_get_media_info)

    client = TestClient(app)

    response = client.post(
        "/api/media/info",
        json={"url": "https://example.com/video"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Unable to extract media information.",
    }


def test_media_download_returns_400_on_extraction_error(monkeypatch):
    def fake_download_media(url: str, format_id: str):
        raise MediaExtractionError("Unable to download this media.")

    monkeypatch.setattr(media_api, "download_media", fake_download_media)

    client = TestClient(app)

    response = client.post(
        "/api/media/download",
        json={
            "url": "https://example.com/video",
            "format_id": "video-720",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Unable to download this media.",
    }
