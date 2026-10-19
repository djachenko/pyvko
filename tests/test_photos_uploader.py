import json
from pathlib import Path
from typing import Any

import pytest
import requests
from vk_api import VkApi

from pyvko.shared.photos_uploader import AlbumPhotoUploader

PHOTO_OBJECT = {"id": 1, "owner_id": -2, "sizes": [], "text": ""}

RESPONSES = {
    "photos.getUploadServer": {"upload_url": "https://upload.example/photos"},
    "photos.save": [PHOTO_OBJECT],
}


class FakeUploadResponse:
    def json(self) -> dict[str, Any]:
        return {"aid": 3, "server": 4, "photos_list": "[]", "hash": "hash"}


@pytest.mark.parametrize("relative", [False, True])
def test_upload_many_accepts_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, relative: bool) -> None:
    photo = tmp_path / "photo.jpg"
    photo.write_bytes(b"jpeg")

    if relative:
        monkeypatch.chdir(tmp_path)
        photo = Path(photo.name)

    sent_names: list[str] = []

    def fake_method(_: VkApi, method: str, values: dict[str, Any] | None = None, **__: Any) -> Any:
        return RESPONSES[method]

    def fake_post(_: requests.Session, url: str, files: list[Any]) -> FakeUploadResponse:
        sent_names.extend(name for _, (name, _) in files)

        return FakeUploadResponse()

    monkeypatch.setattr(VkApi, "method", fake_method)
    monkeypatch.setattr(requests.Session, "post", fake_post)

    uploader = AlbumPhotoUploader(VkApi(token="fake").get_api(), album_id=3, group_id=2)

    photos = uploader.upload_many([photo])

    assert sent_names == ["file0.jpg"]
    assert [photo.id for photo in photos] == [1]


def test_upload_single_photo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    photo = tmp_path / "photo.jpg"
    photo.write_bytes(b"jpeg")

    upload_response = {"photos_list": "[]", "server": 4, "aid": 3, "hash": "hash"}
    calls: list[tuple[str, dict[str, Any]]] = []

    class FakeResponse:
        text = json.dumps(upload_response)

    def fake_method(_: VkApi, method: str, values: dict[str, Any] | None = None, **__: Any) -> Any:
        calls.append((method, values or {}))

        return RESPONSES[method]

    def fake_post(url: str, files: dict[str, Any]) -> FakeResponse:
        return FakeResponse()

    monkeypatch.setattr(VkApi, "method", fake_method)
    monkeypatch.setattr(requests, "post", fake_post)

    uploader = AlbumPhotoUploader(VkApi(token="fake").get_api(), album_id=3, group_id=2)

    uploaded = uploader.upload(photo)

    assert uploaded.id == 1
    assert calls == [
        ("photos.getUploadServer", {"album_id": 3, "group_id": 2}),
        ("photos.save", {"album_id": 3, "group_id": 2} | upload_response),
    ]
