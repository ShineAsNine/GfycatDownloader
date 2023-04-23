import os
import sys
import traceback

import click

from utils.options_helper import GFY_TYPE
from utils.download_gfys import DownloadGfys
from utils.process_options import ProcessOptions
from utils.request_gfys import RequestGfys

from utils.errors import InvalidOutputTemplate, ExpiredOrInvalidAuthKey, InvalidSingleGfyUrl


@click.command()
@click.option("-od", "--output-directory", prompt="Output Directory", type=click.Path(exists=True))
@click.option("-ot", "--output-template", prompt="Output Template", default="Press enter for default")
@click.option("-tf", "--text_file", prompt="Text File", type=click.Path(exists=True))
@click.option("-gt", "--gfy-type-to-download", prompt="Gfy Type To Download:\n 1) MP4\n 2) WebM\n 3) Larger of the two\n", type=click.Choice(GFY_TYPE))
@click.option("-s", "--sleep", prompt="Sleep Between Downloads", type=click.INT)
@click.option("-o", "--overwrite", prompt="Overwrite Existing Gfys (y/n)", type=click.BOOL)
def links_from_txt(output_directory, output_template, text_file, gfy_type_to_download, sleep, overwrite):

    try:
        with open(text_file, "r", encoding="utf-8") as f:
            urls = [line.rstrip() for line in f]

        for url in urls:
            try:
                if "collection" in url:
                    download_options = ProcessOptions(
                        output_directory=output_directory,
                        output_template=output_template,
                        auth_key=None,
                        profile_to_download=None,
                        collection=url,
                        json_file=None,
                        single_gfy=None,
                        gfy_type_to_download=int(gfy_type_to_download),
                        sleep_time=sleep,
                        overwrite=overwrite
                    ).get_options()

                elif "@" in url:
                    download_options = ProcessOptions(
                        output_directory=output_directory,
                        output_template=output_template,
                        auth_key=None,
                        profile_to_download=url,
                        collection=None,
                        json_file=None,
                        single_gfy=None,
                        gfy_type_to_download=int(gfy_type_to_download),
                        sleep_time=sleep,
                        overwrite=overwrite
                    ).get_options()

                else:
                    download_options = ProcessOptions(
                        output_directory=output_directory,
                        output_template=output_template,
                        auth_key=None,
                        profile_to_download=None,
                        collection=None,
                        json_file=None,
                        single_gfy=url,
                        gfy_type_to_download=int(gfy_type_to_download),
                        sleep_time=sleep,
                        overwrite=overwrite
                    ).get_options()

                gfys = RequestGfys(download_options).start_request_loop()

                if gfys is None:
                    print(f"Invalid URL: {url}")
                    continue

                DownloadGfys(download_options, gfys).start_download()

            except InvalidSingleGfyUrl as e:
                print(f"{e.message}: {e.url}")

        os.system("pause")
        sys.exit()

    except KeyboardInterrupt as e:
        os.system("pause")
        sys.exit()

    except (InvalidOutputTemplate, ExpiredOrInvalidAuthKey) as e:
        click.echo(e.message)
        os.system("pause")
        sys.exit()

    except Exception as e:
        click.echo(traceback.format_exc())
        os.system("pause")
        sys.exit()
