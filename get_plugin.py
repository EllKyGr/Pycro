# Use the raw plugin channel JSON to locate the plugin and require it accordingly
from typing import Generator
from requests import get
from requests.exceptions import HTTPError
from argparse import ArgumentParser, Namespace
import json, re

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

entered_plugins: Namespace = parser.parse_args()


def micro_main_channel_plugin(url: str) -> list[str]:
    """
    Returns the main channel JSON file as a list with all available plugins.
    Since the file contains commentaries, this are removed beforehand for proper
    parsing
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

        with open(filename, mode="wb") as file:
            print(f"Downloading {filename}...")
            for chunk in response.iter_content(chunk_size=10 * 1024):
                print(". ", end=' ', flush=True)
                file.write(chunk)
        print()
    else:
        raise HTTPError(f"Unable to reach zip file: {response.status_code}")

    return None


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
            plugin_data: dict[str, str | list] = response.json()
            for info in plugin_data:
                plugin_name: str = info["Name"]
                version: str = info["Versions"][0]["Version"]
                url_zip: str = info["Versions"][0]["Url"]
            print(
                f"Success! {plugin_name}-{version} version. Available at:\n\t{url_zip}"
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
    if entered_plugins.plugin:
        print("Argument detected plugins:", *entered_plugins.plugin)
        required_plugins = verify_plugin(all_plugins, entered_plugins)
    else:
        print("Requiring Pycro recommend plugins...")
        required_plugins = verify_plugin(all_plugins)

    try:
        request_plugin(required_plugins)
    except HTTPError as err:
        print(err)


if __name__ == '__main__':
    main()
