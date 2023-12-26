import requests
import tempfile
import shutil
from github import Github
from github.Repository import Repository
from rich import print
from rich.prompt import Confirm
from version import __version__

def get_repo(repo: str) -> Repository:
    github = Github()
    repo = github.get_repo(repo)
    return repo

def update():
    repo = get_repo("andonihq/cli-tool")

    latest_version = repo.get_tags()[0].name
    current_version = __version__

    if latest_version != current_version:
        print(f"Latest version: [bold][blue]{latest_version}")
        print(f"Current version: [bold][yellow]{current_version}")
        update = Confirm.ask("[yellow]There is a new version, do you want to update?")

    if update:
        latest_release = repo.get_release(latest_version)
        asset = next((asset for asset in latest_release.get_assets() if asset.name == "cli-tool"), None)
        response = requests.get(asset.browser_download_url)
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as new_ver:
            new_ver.write(response.text)
            try:
                shutil.move(new_ver.name, __file__)
                print("[bold][green]Cli-tool updated sucessfully")
            except Exception as e:
                raise SystemExit(f"Error when trying to update: {e}")

    if latest_version == current_version:
        print(f"Latest version: [bold][blue]{latest_version}")
        print(f"Current version: [bold][green]{current_version}")
        print(f"[bold][green]You are up to date.")




    

    