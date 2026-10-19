from pyvko.aspects.albums import Album


def test_group_has_id(test_group):
    assert isinstance(test_group.id, int)
    assert test_group.id != 0


def test_group_has_name(test_group):
    assert isinstance(test_group.name, str)
    assert test_group.name


def test_group_get_members(test_group):
    members = test_group.get_members()

    assert isinstance(members, list)
    assert len(members) > 0


def test_group_get_posts(test_group):
    posts = test_group.get_posts()

    assert isinstance(posts, list)


def test_group_get_albums(test_group):
    albums = test_group.get_all_albums()

    assert isinstance(albums, list)


def test_group_get_album_by_id(test_group, created_album):
    album = test_group.get_album_by_id(created_album.id)

    assert album is not None
    assert isinstance(album, Album)
    assert album.id == created_album.id
