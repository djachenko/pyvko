from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from pyvko.aspects.albums import Album
from pyvko.aspects.groups import Group
from pyvko.attachment.photo import Photo
from pyvko.shared.photos_uploader import AlbumPhotoUploader
from tests.unit.fake_vk import FakeVk, page
from tests.unit.vk_objects import ALBUM_OBJECT, GROUP_ID, PHOTO_OBJECT


class TestAlbums:
    def test_get_all_albums(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "photos.getAlbums": page(ALBUM_OBJECT),
        }

        albums = group.get_all_albums()

        assert [(album.id, album.name) for album in albums] == [(5, "Album")]
        assert vk.params("photos.getAlbums") == {
            "owner_id": -GROUP_ID,
        }

    def test_get_album_by_id(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "photos.getAlbums": page(ALBUM_OBJECT),
        }

        album = group.get_album_by_id(5)

        assert album is not None
        assert album.id == 5
        assert vk.params("photos.getAlbums") == {
            "owner_id": -GROUP_ID,
            "album_ids": [5],
        }

    def test_get_album_by_id_returns_none_when_missing(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "photos.getAlbums": page(),
        }

        assert group.get_album_by_id(5) is None

    def test_create_album(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "photos.createAlbum": ALBUM_OBJECT,
        }

        album = group.create_album("Album")

        assert album.id == 5
        assert vk.params("photos.createAlbum") == {
            "title": "Album",
            "group_id": GROUP_ID,
            "upload_by_admins_only": 1,
        }

    def test_get_photos(self, vk: FakeVk) -> None:
        vk.responses = {
            "photos.get": page(PHOTO_OBJECT),
        }

        photos = Album(vk, ALBUM_OBJECT).get_photos()

        assert [(photo.id, photo.largest_link()) for photo in photos] == [(3, "https://photo/x")]
        assert vk.params("photos.get") == {
            "owner_id": -GROUP_ID,
            "album_id": 5,
            "offset": 0,
        }

    def test_add_photos(self, vk: FakeVk, monkeypatch: pytest.MonkeyPatch) -> None:
        uploads: list[tuple[Any, int, list[Path]]] = []

        def fake_upload_many(uploader: AlbumPhotoUploader, paths: list[Path]) -> list[Photo]:
            uploads.append((uploader.new_api, uploader.get_params()["group_id"], paths))

            return [Photo.from_photo_object(vk, PHOTO_OBJECT)]

        monkeypatch.setattr(AlbumPhotoUploader, "upload_many", fake_upload_many)

        photo = Album(vk, ALBUM_OBJECT).add_photo(Path("photo.jpg"))

        assert photo.id == 3
        assert uploads == [(vk, GROUP_ID, [Path("photo.jpg")])]

    def test_attachment(self, vk: FakeVk) -> None:
        album = Album(vk, ALBUM_OBJECT)

        assert album.to_attach() == f"album-{GROUP_ID}_5"
        assert album.url == f"https://vk.com/album-{GROUP_ID}_5"
