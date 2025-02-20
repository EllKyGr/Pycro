#!/usr/bin/env python3
# Use the raw plugin channel JSON to locate the plugin and require it accordingly
import json, re
from pathlib import Path
from requests import get
from typing import Generator
from requests.exceptions import HTTPError
from argparse import ArgumentParser, Namespace

MC_URL: str = "https://raw.githubusercontent.com/micro-editor/plugin-channel/master/channel.json"
PYCRO_PLUGINS: list[str] = [
    "aspell",
    "cheat",
    "filemanager",
    "lsp",
    "manipulator",
    "quoter",
    "runit",
    "snippets",
]

parser: ArgumentParser = ArgumentParser(
    prog="Plugin Retriever",
    description="Requests the plugin(s) from Micro's main channel and downloads"
    " them if, for whatever reason, Micro's `-plugin` command fails",
    epilog="Refer to `https://github.com/micro-editor/plugin-channel` or"
    " `https://micro-editor.github.io/plugins.html` to prevent"
    " typos during retrieval, i.e. aspel instead of aspell")

parser.add_argument(
    "-pl",
    "--plugin",
    nargs="+",
    help="User required plugin(s) for Micro. At least one must be entered",
)

parser.add_argument(
    "-dir",
    "--directory",
    action="store_true",
    help=
    "If flag given, downloads the required plugins at ~/.config/micro/plug over"
    " current script location. No additional arguments required.",
)

args: Namespace = parser.parse_args()


def micro_main_channel_plugin(url: str) -> list[str]:
    """
    Returns the main channel JSON file as a list with all available plugins.
    Since the file contains commentaries, these are removed beforehand for
    proper parsing
    :param url: Micro's main channel Url
    :return: JSON object with all url plugins
    """
    response = get(url)

    if response.status_code == 200:
        print("Accessing Micro's main plugin channel...")
    else:
        raise HTTPError(
            f"Unable to access main channel: {response.status_code}")

    response_wo_comments = re.sub("\\s//.*",
                                  "",
                                  response.text,
                                  flags=re.MULTILINE)

    return json.loads(response_wo_comments)


def verify_plugin(
        channel_plugins: list[str],
        plarg: Namespace | list[str] = PYCRO_PLUGINS) -> Generator[str]:
    """
    Loop through the main channel list in order to select the desired ones, then
    yield the respective JSON file url
    :param channel_plugins: all registered plugins in the main Micro channel
    :param plarg: Default list with recommend plugins or user entered plugins as
        an argument
    :return: one time use plugin url
    """
    if isinstance(plarg, Namespace):
        for plugin in plarg.plugin:
            for plugin_link in channel_plugins:
                if plugin in plugin_link:
                    print(
                        f"\n'{plugin}' found in main channel, requesting file..."
                    )
                    yield plugin_link
    else:
        for plugin in plarg:
            for plugin_link in channel_plugins:
                if plugin in plugin_link:
                    print(
                        f"\n'{plugin}' found in main channel, requesting file..."
                    )
                    yield plugin_link

    print()


def save_at_plug_dir(zip_file: str) -> str:
    """
    If the argument `-dir` is given saves the required zip files directly at
    `~/.config/micro/plug`
    :zip_file: string representation of the zip file.
    :return: absolute path including zip file for saving.
    """
    script_location: Path = Path(__file__).absolute().parent
    parent_path: list[str] = str(script_location).split("/")
    relative_plug_dir: list[str] = (".config/micro/plug/" +
                                    zip_file).split("/")

    home_position: int = parent_path.index("home")
    if parent_path[home_position - 1] != "files":  # Not a Termux path
        home_position += 1

    absolute_plug_path = parent_path[:home_position + 1] + relative_plug_dir
    plugin_location: str = '/'.join(absolute_plug_path)

    return plugin_location


def request_zip(url: str) -> None:
    """
    Request the zip from the plugin JSON file
    :param url: JSON file url from each plugin
    :return: None
    """
    response = get(url, stream=True)
    if response.status_code == 200:
        if "content-disposition" in response.headers:
            content_disposition = response.headers["content-disposition"]
            filename: str = content_disposition.split("filename=")[1]
        else:
            filename = url.split("/")[-1]
        if args.directory:
            filename = save_at_plug_dir(filename)
        with open(filename, mode="wb") as file:
            print(f"Downloading {filename.split('/')[-1]}...")
            for chunk in response.iter_content(chunk_size=10 * 1024):
                print(". ", end=' ', flush=True)
                file.write(chunk)
        print()
    else:
        raise HTTPError(f"Unable to reach zip file: {response.status_code}")


def grab_latest_version(
        json_data: list[dict[str, str | list]]) -> tuple[str, str]:
    """
     In case more than one version exists in the JSON file and the order of them
     is not consistent, i.e. the latest version instead of being at the top it
     is at the bottom.
     :param json_data: all the metadata from the plugin
     :return: the latest url zip version
     """
    zip_url: str
    version: str
    versions: dict = json_data[0]['Versions']
    total_ver: int = len(versions)
    if total_ver > 1:
        last_entered_version: tuple = tuple(versions[total_ver - 1].items())
        first_position_version: tuple = tuple(versions[0].items())

        if last_entered_version[0] > first_position_version[0]:
            zip_url = last_entered_version[1][1]
            version = last_entered_version[0][1]
        else:
            zip_url = first_position_version[1][1]
            version = first_position_version[0][1]
    else:
        plugin_data: tuple = tuple(versions[0].items())
        zip_url = plugin_data[1][1]
        version = plugin_data[0][1]

    return zip_url, version


def request_plugin(plugin_url: Generator[str]) -> None:
    """
    Access to the JSON file for each plugin if previously found. Retrieve the
    name, latest version and zip file link.
    :plugin_url: JSON file url containing plugin's metadata
    :return: None
    """
    for plugin in plugin_url:
        response = get(plugin)
        if response.status_code == 200:
            plugin_data: list[dict] = response.json()
            name: str = plugin_data[0]['Name']
            url_zip, version = grab_latest_version(plugin_data)
            print(
                f"Success! {name}-{version} version. Available at:\n\t{url_zip}"
            )
            try:
                request_zip(url_zip)
            except HTTPError as err:
                print(err)

        else:
            raise HTTPError(
                f"Unable to reach plugin file: {response.status_code}")


def main() -> None:
    try:
        all_plugins: list[str] = micro_main_channel_plugin(MC_URL)
    except HTTPError as err:
        print(err)

    required_plugins: Generator[str]
    if args.plugin:
        print("Argument detected with user plugins:", *args.plugin)
        required_plugins = verify_plugin(all_plugins, args)
    else:
        print("Requiring Pycro recommend plugins...")
        required_plugins = verify_plugin(all_plugins)

    try:
        request_plugin(required_plugins)
    except HTTPError as err:
        print(err)


if __name__ == '__main__':
    main()
