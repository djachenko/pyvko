from pathlib import Path

from post import Post
from pyvko import Pyvko
from photos_uploader import PhotosUploader


def main():
    pyvko = Pyvko()

    test_group = pyvko.get_group("pyvko_test2")

    uploader = PhotosUploader(pyvko.api)

    photo_paths = [path for path in Path("test_photos").iterdir()]

    photos = [uploader.upload_to_wall(test_group.id, path) for path in photo_paths]

    post = Post(text="post w 2 img", attachments=photos)

    test_group.add_post(post)


    # uploader.upload_to_album(264162929, test_group.id, photo)

    a = 7


if __name__ == '__main__':
    main()
