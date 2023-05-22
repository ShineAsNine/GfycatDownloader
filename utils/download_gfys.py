import os
import sys
import time
import traceback
from datetime import datetime

import click
import requests
from tqdm import tqdm

requests.packages.urllib3.disable_warnings()  # type: ignore


class DownloadGfys():
    def __init__(self, download_options, gfys):
        self.output_directory = download_options.get("output_directory")
        self.output_template = download_options.get("output_template")
        self.auth_key = download_options.get("auth_key")
        self.profile_to_download = download_options.get("profile_to_download")
        self.collection = download_options.get("collection")
        self.private_collection = download_options.get("private_collection")
        self.own_likes = download_options.get("own_likes")
        self.user_likes = download_options.get("user_likes")
        self.json_file = download_options.get("json_file")
        self.single_gfys = download_options.get("single_gfy")
        self.gfys = self.json_file if self.json_file is not None else gfys
        self.gfy_type_to_download = download_options.get("gfy_type_to_download")
        self.sleep_time = download_options.get("sleep_time")
        self.overwrite = download_options.get("overwrite")

    def start_download(self):
        try:
            directory_name = self.create_directory()

            total_gfys = len(self.gfys)

            gfys_downloaded = 0

            for gfy in self.gfys:
                try:
                    upload_date = datetime.fromtimestamp(
                        gfy.get("createDate")).strftime("%y%m%d")
                    mp4_size = gfy.get("mp4Size")
                    webm_size = gfy.get("webmSize")
                    self.download_ext = self.get_download_ext(mp4_size, webm_size)
                    title = gfy.get("title")
                    gfy_id = gfy.get("gfyName")
                    likes = gfy.get("likes")
                    frame_rate = gfy.get("frameRate")
                    height = gfy.get("height")
                    width = gfy.get("width")
                    views = gfy.get("views")
                    username = gfy.get("username")
                    number_of_frames = gfy.get("numFrames")
                    length = f"{str(round(number_of_frames / frame_rate, 2))} Seconds"
                    frame_rate = str(round(frame_rate, 0))

                    filename = self.get_filename(
                        username, upload_date, title, length, gfy_id, likes, frame_rate, height, width, views)

                    if directory_name:
                        full_output = os.path.join(
                            self.output_directory, directory_name, f"{filename}{self.download_ext}")
                    else:
                        full_output = os.path.join(
                            self.output_directory, f"{filename}{self.download_ext}")

                    if self.overwrite is False and os.path.exists(full_output):
                        click.echo(
                            f"Already Downloaded: {gfys_downloaded + 1} of {total_gfys} https://gfycat.com/{gfy_id}")
                        gfys_downloaded += 1
                        continue

                    self.download_gfy(full_output, filename, gfy, total_gfys, gfys_downloaded)

                    if os.path.exists(full_output):
                        gfys_downloaded += 1

                    time.sleep(self.sleep_time)

                except KeyboardInterrupt as e:
                    click.echo(f"\n\nDownloaded Stopped | Downloaded {gfys_downloaded} of {total_gfys} gfys")
                    tqdm._instances.clear()  # type: ignore
                    os.system("pause")
                    sys.exit()

                except Exception as e:
                    click.echo(traceback.format_exc())
                    continue

            time.sleep(1)
            click.echo(
                f"Download Finished | Downloaded {gfys_downloaded} of {total_gfys} gfys")

        except Exception as e:
            click.echo(traceback.format_exc())

    def create_directory(self):
        if self.auth_key or self.profile_to_download:
            self.url = "https://api.gfycat.com/v1/me/gfycats"
            username = self.gfys[0].get("username")
            os.makedirs(os.path.join(self.output_directory, username), exist_ok=True)
            return username
        elif self.collection:
            collection_username = self.collection[0]
            collection_id = self.collection[1]
            collection_directory = f"{collection_username} - {collection_id}"
            os.makedirs(os.path.join(self.output_directory, collection_directory), exist_ok=True)
            return collection_directory
        elif self.private_collection:
            collection_username = self.private_collection[0]
            collection_id = self.private_collection[1]
            collection_directory = f"{collection_username} - {collection_id}"
            os.makedirs(os.path.join(self.output_directory, collection_directory), exist_ok=True)
            return collection_directory
        elif self.own_likes is not None:
            headers = {'Authorization': self.own_likes}
            response = requests.get('https://api.gfycat.com/v1/me/likes', headers=headers, verify=False)
            own_likes_directory = f"{response.json()['likes'][0]['username']} - likes"
            os.makedirs(os.path.join(self.output_directory, own_likes_directory), exist_ok=True)
            return own_likes_directory
        elif self.user_likes is not None:
            username_likes = f"{self.gfys[0].get('username')} - likes"
            os.makedirs(os.path.join(self.output_directory, username_likes), exist_ok=True)
            return username_likes
        elif self.json_file is not None:
            return None

    def get_download_ext(self, mp4_size, webm_size):
        if self.gfy_type_to_download == "larger":
            return ".mp4" if mp4_size > webm_size else ".webm"
        elif self.gfy_type_to_download == "mp4":
            return ".mp4"
        elif self.gfy_type_to_download == "webm":
            return ".webm"

    def get_filename(self, username, upload_date, title, length, gfy_id, likes, frame_rate, height, width, views):
        filename = self.output_template % {
            'upload_date': upload_date,
            'title': title,
            'length': length,
            'gfy_id': gfy_id,
            'likes': likes,
            'frame_rate': frame_rate,
            'height': height,
            'width': width,
            'views': views
        }

        total_length = len(self.output_directory + username + filename + self.download_ext)

        if total_length > 259:
            if "%(title)s" in self.output_template:
                remove_character_from_title = total_length - 259
                filename = self.output_template % {
                    'upload_date': upload_date,
                    'title': title[:-remove_character_from_title],
                    'length': length,
                    'gfy_id': gfy_id,
                    'likes': likes,
                    'frame_rate': frame_rate,
                    'height': height,
                    'width': width,
                    'views': views
                }
            else:
                filename = filename[:259]

        return self.validate_filename(filename)

    def validate_filename(self, filename):
        invalid_chars = "<>:\"/\\|?*"
        for c in invalid_chars:
            filename = filename.replace(c, "_")
        filename = filename.rstrip(".")
        return filename

    def download_gfy(self, output, filename, gfy, total_gfys, gfys_downloaded):
        if self.download_ext == ".mp4":
            download_url = gfy.get("mp4Url")
        else:
            download_url = gfy.get("webmUrl")

        response = requests.get(download_url, stream=True, verify=False)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024

        click.echo(f"Downloading: {gfys_downloaded + 1} of {total_gfys} | {filename}")
        progress_bar = tqdm(total=total_size_in_bytes,
                            unit='iB', unit_scale=True, ncols=75)
        with open(output, 'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            click.echo("ERROR, something went wrong")
