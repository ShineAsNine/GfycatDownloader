import json
from re import search
from urllib.parse import urlparse

import requests
import validators
from utils.errors import InvalidOutputTemplate, InvalidProfile, InvalidCollection, InvalidSingleGfyUrl


class ProcessOptions:
    def __init__(self, output_directory,
                 output_template, auth_key,
                 profile_to_download, collection,
                 private_collection, own_likes,
                 user_likes, json_file, single_gfy,
                 gfy_type_to_download, sleep_time,
                 overwrite):
        self.output_directory = output_directory
        self.output_template = output_template
        self.auth_key = auth_key
        self.profile_to_download = profile_to_download
        self.collection = collection
        self.private_collection = private_collection
        self.own_likes = own_likes
        self.user_likes = user_likes
        self.json_file = json_file
        self.single_gfy = single_gfy
        self.gfy_type_to_download = gfy_type_to_download
        self.sleep_time = sleep_time
        self.overwrite = overwrite

    def get_options(self) -> dict:
        profile_to_download = self.process_profile() if self.profile_to_download is not None else None
        collection = self.process_collection() if self.collection is not None else None
        private_collection = self.process_private_collection() if self.private_collection is not None else None
        user_likes = self.process_user_likes() if self.user_likes is not None else None
        json_file = self.process_json_file() if self.json_file is not None else None
        single_gfy = self.process_single_gfy() if self.single_gfy is not None else None

        return {
            "output_directory": self.output_directory,
            "output_template": self.process_output_template(),
            "auth_key": self.auth_key,
            "profile_to_download": profile_to_download,
            "collection": collection,
            "private_collection": private_collection,
            "own_likes": self.own_likes,
            "user_likes": user_likes,
            "json_file": json_file,
            "single_gfy": single_gfy,
            "gfy_type_to_download": self.process_gfy_type_to_download(),
            "sleep_time": self.sleep_time,
            "overwrite": self.overwrite
        }

    def process_output_template(self):
        try:
            if self.output_template == "Press enter for default":
                return "%(upload_date)s - %(title)s [%(gfy_id)s]"

            _ = self.output_template % {
                'upload_date': "upload_date",
                'title': "title",
                'gfy_id': "gfyId",
                'likes': "likes",
                'frame_rate': "frameRate",
                'height': "height",
                'width': "width",
                'views': "views"
            }

            return self.output_template

        except (KeyError, ValueError) as e:
            raise InvalidOutputTemplate from e

    def process_profile(self):
        if validators.url(self.profile_to_download):
            url = self.profile_to_download
        else:
            url = f"https://gfycat.com/@{self.profile_to_download}"

        return self.validate_profile(url)
        # return f"https://gfycat.com/@{self.profile_to_download}"

    def validate_profile(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise InvalidProfile
        return urlparse(url).path[1:].split("/")[0][1:]

    def process_collection(self):
        valid_url = validators.url(self.collection)
        if valid_url is True:
            return self.validate_collection(self.collection)
        else:
            raise InvalidCollection

    def validate_collection(self, url):
        parsed_url = urlparse(url).path[1:].split("/")
        username = parsed_url[0][1:]

        if parsed_url[2] == "collections":
            collection_id = parsed_url[3]
        else:
            collection_id = parsed_url[2]

        url = f"https://api.gfycat.com/v1/users/{username}/collections/{collection_id}/gfycats"

        response = requests.get(url)
        if response.status_code != 200:
            raise InvalidCollection

        return username, collection_id

    def process_private_collection(self):
        valid_url = validators.url(self.private_collection[0])
        if valid_url is True:
            return self.validate_private_collection(self.private_collection)
        else:
            raise InvalidCollection

    def validate_private_collection(self, url_auth):
        url = url_auth[0]
        auth_key = url_auth[1]

        parsed_url = urlparse(url).path[1:].split("/")
        username = parsed_url[0][1:]

        if parsed_url[2] == "collections":
            collection_id = parsed_url[3]
        else:
            collection_id = parsed_url[2]

        headers = {'Authorization': auth_key}
        url = f"https://api.gfycat.com/v1/me/collections/{collection_id}/gfycats"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise InvalidCollection

        return username, collection_id, auth_key

    def process_user_likes(self):
        if validators.url(self.user_likes):
            if "/likes" in self.user_likes:
                url = self.user_likes
            else:
                url = f"{self.user_likes}/likes"
        else:
            url = f"https://gfycat.com/@{self.user_likes}/likes"

        return self.validate_profile_likes(url)
        # return f"https://gfycat.com/@{self.profile_to_download}"

    def validate_profile_likes(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise InvalidProfile
        return urlparse(url).path[1:].split("/")[0][1:]

    def process_json_file(self):
        with open(self.json_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def process_single_gfy(self):
        if not (gfycat_id := search(r'/([\w-]+)', urlparse(self.single_gfy).path)):
            raise InvalidSingleGfyUrl(self.single_gfy)

        gfycat_id = gfycat_id[1]
        if "-" in gfycat_id and not gfycat_id.endswith((".mp4", ".webm")):
            gfycat_id = gfycat_id.split("-")[0]

        return gfycat_id

    def process_gfy_type_to_download(self):
        if self.gfy_type_to_download == 1:
            return "mp4"
        elif self.gfy_type_to_download == 2:
            return "webm"
        elif self.gfy_type_to_download == 3:
            return "larger"
