import requests
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
            try:
                latest_release = repo.get_release(latest_version)
                for asset in latest_release.get_assets():
                    if asset.name == "cli-tool":
                        print(asset.browser_download_url)
                        response = requests.get(asset.browser_download_url)
                        open("cli-tool", "wb").write(response.content)
            except Exception as e:
                print(f"Couldn't update sucessfully: {e}")

    if latest_version == current_version:
        print(f"Latest version: [bold][blue]{latest_version}")
        print(f"Current version: [bold][green]{current_version}")
        print(f"[bold][green]You are up to date.")

    

    