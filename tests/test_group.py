import pytest

from pyvko.aspects.albums import Album


class TestExistingGroup:
    def test_has_id(self, test_group):
        assert isinstance(test_group.id, int)
        assert test_group.id != 0

    def test_has_name(self, test_group):
        assert isinstance(test_group.name, str)
        assert test_group.name

    def test_get_members(self, test_group):
        members = test_group.get_members()

        assert isinstance(members, list)
        assert len(members) > 0

    def test_get_posts(self, test_group):
        posts = test_group.get_posts()

        assert isinstance(posts, list)

    def test_get_albums(self, test_group):
        albums = test_group.get_all_albums()

        assert isinstance(albums, list)


@pytest.mark.create
class TestGroupWithCreatedAlbum:
    def test_get_album_by_id(self, test_group, created_album):
        album = test_group.get_album_by_id(created_album.id)

        assert album is not None
        assert isinstance(album, Album)
        assert album.id == created_album.id
