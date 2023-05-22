import traceback

import click
import requests
from requests.adapters import Retry, HTTPAdapter

from utils.errors import ExpiredOrInvalidAuthKey


class AllCollections:
    def __init__(self, auth_key, username):
        if auth_key:
            self.auth_key = auth_key
            self.url = "https://api.gfycat.com/v1/me/collections"
        elif username:
            self.auth_key = None
            self.url = f"https://api.gfycat.com/v1/users/{username}/collections"

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

        urls = []

        headers = {'Authorization': self.auth_key}
        params = {"count": "100"}

        while True:
            try:
                (r := session.get(self.url, headers=headers, params=params)).raise_for_status()

                response = r.json()

                for collection in response["gfyCollections"]:
                    is_published = collection["published"]
                    folder_id = collection["folderId"]
                    username = collection["userId"]
                    if is_published == 0:
                        urls.append((f"https://gfycat.com/@{username}/collections/{folder_id}", self.auth_key))
                    else:
                        urls.append(f"https://gfycat.com/@{username}/collections/{folder_id}")

                if cursor := response.get("cursor"):
                    params["cursor"] = cursor

                else:
                    click.echo(f"Total Collections Found: {len(urls)}")
                    return urls

            except requests.exceptions.RetryError as e:
                retry_count = e.last_attempt.attempt_number  # type: ignore
                print(f"Request failed, retry attempt {retry_count}")
                continue
