import pytest


@pytest.mark.create
def test_album_created(created_album):
    assert isinstance(created_album.id, int)
    assert created_album.id > 0


@pytest.mark.create
def test_album_has_name(created_album):
    assert created_album.name == "pyvko test album"


@pytest.mark.create
def test_get_album_by_id(test_group, created_album):
    album = test_group.get_album_by_id(created_album.id)

    assert album is not None
    assert album.id == created_album.id


@pytest.mark.create
def test_photo_uploaded(uploaded_photo):
    assert isinstance(uploaded_photo.id, int)
    assert uploaded_photo.id > 0


@pytest.mark.create
def test_photo_has_url(uploaded_photo):
    url = uploaded_photo.largest_link()

    assert url
    assert url.startswith("https://")


@pytest.mark.create
def test_album_get_photos_contains_uploaded(created_album, uploaded_photo):
    photos = created_album.get_photos()
    photo_ids = [p.id for p in photos]

    assert uploaded_photo.id in photo_ids


@pytest.mark.create
def test_set_album_cover(created_album, uploaded_photo):
    created_album.set_cover(uploaded_photo)
