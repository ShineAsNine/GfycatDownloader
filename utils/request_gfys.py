import json
import time
import traceback
from datetime import datetime

import click
import requests
from requests.adapters import Retry, HTTPAdapter

from utils.errors import ExpiredOrInvalidAuthKey


class RequestGfys:

    def __init__(self, download_options):
        self.auth_key = download_options.get("auth_key")
        self.profile_to_download = download_options.get("profile_to_download")
        self.collection = download_options.get("collection")
        self.private_collection = download_options.get("private_collection")
        self.own_likes = download_options.get("own_likes")
        self.user_likes = download_options.get("user_likes")
        self.single_gfy = download_options.get("single_gfy")
        self.sleep_time = download_options.get("sleep_time")

        if self.auth_key is not None:
            self.url = "https://api.gfycat.com/v1/me/gfycats"
        elif self.profile_to_download is not None:
            self.url = f"https://api.gfycat.com/v1/users/{self.profile_to_download}/gfycats"
        elif self.collection is not None:
            self.collection_username = self.collection[0]
            self.collection_id = self.collection[1]
            self.url = f"https://api.gfycat.com/v1/users/{self.collection_username}/collections/{self.collection_id}/gfycats"
        elif self.private_collection is not None:
            self.collection_username = self.private_collection[0]
            self.collection_id = self.private_collection[1]
            self.collection_auth_key = self.private_collection[2]
            self.url = f"https://api.gfycat.com/v1/me/collections/{self.collection_id}/gfycats"
        elif self.own_likes is not None:
            self.url = "https://api.gfycat.com/v1/me/likes/populated"
        elif self.user_likes is not None:
            self.url = f"https://api.gfycat.com/v1/users/{self.user_likes}/likes/populated"
        elif self.single_gfy is not None:
            self.url = f"https://api.gfycat.com/v1/gfycats/{self.single_gfy}"

    def start_request_loop(self):
        try:
            with requests.session() as session:
                return self.request_loop(session)
        except requests.exceptions.HTTPError as e:
            if str(e).startswith("401"):
                raise ExpiredOrInvalidAuthKey from e
        except Exception as e:
            click.echo(traceback.format_exc())

    def request_loop(self, session):
        retry = Retry(
            total=5,
            status_forcelist=[500, 502, 503, 504],
            backoff_factor=0.1
        )
        session.mount(self.url, HTTPAdapter(max_retries=retry))

        gfys = []
        total_gfys = 0

        if self.auth_key:
            headers = {'Authorization': self.auth_key}
        elif self.own_likes:
            headers = {'Authorization': self.own_likes}
        elif self.private_collection:
            headers = {'Authorization': self.collection_auth_key}
        else:
            headers = None

        params = {"count": "100"}

        while True:
            try:
                (response := session.get(self.url, headers=headers,
                 params=params)).raise_for_status()

                json_response = response.json()

                if self.single_gfy:
                    gfys.append(json_response["gfyItem"])
                    return gfys

                gfys_found = len(json_response["gfycats"])
                total_gfys += gfys_found
                gfys.extend(json_response["gfycats"])
                click.echo(f"Found {gfys_found} gfys - Total: {total_gfys}")

                if cursor := json_response.get("cursor"):
                    params["cursor"] = cursor

                else:
                    click.echo(f"Total Gfys: {total_gfys}")

                    self.create_json(gfys)

                    return (gfys)

                time.sleep(self.sleep_time)

            except requests.exceptions.RetryError as e:
                retry_count = e.last_attempt.attempt_number  # type: ignore
                click.echo(f"Request failed, retry attempt {retry_count}")
                continue

    def create_json(self, gfys):
        current_date = datetime.now().strftime("%y%m%d")
        if self.auth_key or self.profile_to_download:
            self.json_name = gfys[0]['username']
        elif self.collection or self.private_collection:
            self.json_name = f"{self.collection_username} - {self.collection_id}"
        elif self.own_likes:
            headers = {'Authorization': self.own_likes}
            response = requests.get('https://api.gfycat.com/v1/me/likes', headers=headers)
            self.json_name = f"{response.json()['likes'][0]['username']} - likes"
        elif self.user_likes:
            self.json_name = f"{gfys[0]['username']} - likes"

        with open(f"./{current_date} {self.json_name}.json", "w", encoding="utf-8") as f:
            json.dump(gfys, f, indent=4)
