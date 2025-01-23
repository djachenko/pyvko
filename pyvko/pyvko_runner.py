import json
import random
from datetime import timedelta, datetime, date, time
from pathlib import Path
from time import sleep

from pyvko.aspects.albums import Album
from pyvko.aspects.events import Event
from pyvko.config.config import Config
from pyvko.aspects.posts import Post
from pyvko.pyvko_main import Pyvko


def test_uploading(pyvko: Pyvko):
    test_group = pyvko.groups.get_group("mothilda")

    photo_paths = [path for path in Path("../test_photos").iterdir()][:3]

    photos = [test_group.upload_photo_to_wall(path) for path in photo_paths]

    post = Post(text="post w 2 img", attachments=photos)

    test_group.add_post(post)


def create_scheduled_posts():
    start_date = date.today() + timedelta(days=3)

    step = timedelta(days=8)

    for i in range(20):
        post_date = start_date + step * i
        post_time = time(
            hour=random.randint(8, 23),
            minute=random.randint(0, 59),
        )

        post_datetime = datetime.combine(post_date, post_time)

        print(post_datetime)

        post = Post(
            text=f"post {i}\n\n{post_datetime}",
            date=post_datetime
        )

        # test_group.add_post(post)


def test_creating_posts(pyvko: Pyvko):
    test_group = pyvko.groups.get_group("pyvko_test2")

    scheduled = test_group.get_scheduled_posts()

    start_date = scheduled[0].date.date()

    step = timedelta(days=2)

    for i, post in enumerate(scheduled):
        new_post_date = start_date + step * i

        if post.date.date() == new_post_date:
            continue

        new_post_time = post.date.time()

        new_post_datetime = datetime.combine(new_post_date, new_post_time)

        post.date = new_post_datetime
        post.text += f"\n{step.days}: {new_post_datetime}"

        test_group.update_post(post)

        print(f"updated {post.id}")

        sleep(random.randint(10, 20))


def test_posting_album(pyvko: Pyvko):
    group = pyvko.get_by_url("mothilda")

    photoset_path = Path("C:/Users/justin/photos/stages/stage2.develop/20.12.05.miss_stc/progress/")

    post_config_path = photoset_path / "post_config.json"

    with post_config_path.open() as post_config_file:
        post_config = json.load(post_config_file)

    cover_name = post_config["cover"]

    photos_folder = photoset_path / "justin"
    photo_paths = list(photos_folder.iterdir())[:10]

    photos = [group.upload_photo_to_wall(path) for path in photo_paths]

    # new_album = group.create_album(photoset_path.name)
    #
    # for photo_path in list(photos_folder.iterdir())[:10]:
    # photo = new_album.add_photo(photo_path)
    #
    #     print(f"uploaded {photo_path.stem}")
    #
    #     if photo_path.stem == cover_name:
    #         new_album.set_cover(photo)
    #
    #         print("set as cover")

    post = Post(
        text="Ololo2",
        attachments=photos
    )

    group.add_post(post)


def get_all_members(pyvko: Pyvko):
    group = pyvko.get_by_url("test")

    members = group.get_members()
    posts = group.get_posts()

    a = 7


def create_event(pyvko: Pyvko):
    groups = pyvko.groups
    group = groups.get_group("jvstin")
    event = group.create_event("this is test")
    now = datetime.now()
    event.name = f"Renamed event {now}"
    event.event_category = Event.Category.CIRCUS
    event.start_date = now + timedelta(hours=2)
    event.end_date = now + timedelta(hours=2, minutes=30)
    for section in Event.Section:
        event.set_section_state(section, Event.SectionState.DISABLED)
    event.set_section_state(Event.Section.PHOTOS, Event.SectionState.LIMITED)
    event.set_section_state(Event.Section.WALL, Event.SectionState.LIMITED)
    event.is_closed = True
    event.main_section = Event.Section.PHOTOS
    event.save()


def append_album(pyvko: Pyvko):
    justin = pyvko.get_group("jvstin")

    post = justin.get_post(3917)

    post.attachments.append(Album(pyvko.api, {
        "title": "24.10.27.ff_init_forest",
        "id": "303478601",
        "owner_id": "-100568944",
    }))

    justin.update_post(post)


def main():
    pyvko = Pyvko(Config.read(Path("config/config.json")))

    append_album(pyvko)

    a = 7


if __name__ == '__main__':
    main()
