from pathlib import Path

from pyvko import Pyvko
from photos_uploader import PhotosUploader


def main():
    pyvko = Pyvko()

    test_group = pyvko.get_group("pyvko_test")

    uploader = PhotosUploader(pyvko.api)

    photo = [path for path in Path("test_photos").iterdir()][0]

    # uploader.upload_to_wall(test_group.id, photo)
    uploader.upload_to_album(264162929, test_group.id, photo)

    a = 7


if __name__ == '__main__':
    main()
