from abc import abstractmethod, ABC
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

from pyvko.api_based import ApiMixin
from pyvko.attachment.photo import Photo
#
from pyvko.models.models import Post
from pyvko.photos.album import Album
from pyvko.photos.photos_uploader import PhotoUploader, WallPhotoUploader
from pyvko.shared.utils import get_all


class Events(ApiMixin, ABC):
    # noinspection PyUnresolvedReferences
    def create_event(self, title: str) -> 'Event':
        request = self.get_request({
            "title": title,
            "type": "event",
        })

        response = self.api.groups.create(**request)

        event = self.get_event(response["id"])

        return event

    # noinspection PyUnresolvedReferences
    def get_event(self, url: str) -> Optional['Event']:
        from pyvko.models.active_models import Event

        group_request = self.get_request({
            "group_id": url,
            "fields": [
                "start_date",
                "finish_date",
            ]
        })

        event_request = {
            "fields": [
                "start_date",
                "finish_date",
                "main_section",
            ]
        }

        event_request.update(group_request)

        event_response = self.api.groups.getById(**event_request)

        settings_response = self.api.groups.getSettings(**group_request)

        event = Event(self.api, event_object=event_response[0], settings_object=settings_response)

        return event


class Albums(ApiMixin):
    @property
    @abstractmethod
    def id(self) -> int:
        pass

    def __get_albums(self, parameters: Dict = None) -> List[Album]:
        request = self.__get_owned_request(parameters)

        result = self.api.photos.getAlbums(**request)

        albums = [Album(self.api, album_object) for album_object in result["items"]]

        return albums

    def get_all_albums(self) -> List[Album]:
        return self.__get_albums()

    def get_album_by_id(self, album_id: int) -> Album:
        albums_list = self.__get_albums({
            "album_ids": [album_id]
        })

        assert len(albums_list) == 1

        return albums_list[0]

    def create_album(self, name: str) -> Album:
        parameters = {
            "title": name,
            "group_id": self.id,
            "upload_by_admins_only": 1
        }

        parameters = self.get_request(parameters)

        response = self.api.photos.createAlbum(**parameters)

        created_album = Album(self.api, response)

        return created_album

    def __get_owned_request(self, parameters: Dict = None) -> dict:
        if parameters is None:
            parameters = {}
        else:
            parameters = parameters.copy()

        assert "owner_id" not in parameters

        parameters.update({
            "owner_id": -self.id
        })

        return self.get_request(parameters)


class Wall(ApiMixin):
    @property
    @abstractmethod
    def id(self) -> int:
        pass

    def __get_posts(self, parameters: Dict) -> List[Post]:
        parameters = self.__get_owned_request(parameters)

        posts_descriptions = get_all(parameters, self.api.wall.get)

        posts = [Post.from_post_object(description) for description in posts_descriptions]

        return posts

    def get_posts(self) -> List[Post]:
        return self.__get_posts({})

    def get_scheduled_posts(self) -> List[Post]:
        return self.__get_posts({"filter": "postponed"})

    def add_post(self, post: Post) -> int:
        request = self.__get_post_request(post)

        result = self.api.wall.post(**request)

        post_id = result["post_id"]

        return post_id

    def update_post(self, post: Post):
        request = self.__get_post_request(post)

        self.api.wall.edit(**request)

    def delete_post(self, post_id):
        request = self.__get_owned_request({
            "post_id": post_id
        })

        self.api.wall.delete(**request)

    @lru_cache()
    def __get_wall_uploader(self) -> PhotoUploader:
        return WallPhotoUploader(self.api, self.id)

    def upload_photo_to_wall(self, path: Path) -> Photo:
        uploader = self.__get_wall_uploader()

        return uploader.upload(path)

    def __get_post_request(self, post: Post):
        parameters = {
            "from_group": 1
        }

        parameters.update(post.to_request())

        request = self.__get_owned_request(parameters)

        return request

    def __get_owned_request(self, parameters: Dict = None) -> dict:
        if parameters is None:
            parameters = {}
        else:
            parameters = parameters.copy()

        assert "owner_id" not in parameters

        parameters.update({
            "owner_id": -self.id
        })

        return self.get_request(parameters)


class Groups(ApiMixin, ABC):
    # noinspection PyUnresolvedReferences
    def get_group(self, url: str) -> 'Group':
        from pyvko.models.active_models import Group

        group_request = self.get_request({
            "group_id": url
        })

        group_response = self.api.groups.getById(**group_request)

        group = Group(api=self.api, group_object=group_response[0])

        return group
