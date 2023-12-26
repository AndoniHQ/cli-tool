import typer
import boto3
import json
from github import Github
from updater import update
from version import __version__
from rich import print
from rich.panel import Panel
from rich.text import Text

app = typer.Typer()

def version_callback(value: bool):
    if value:
        print(f"[bold]cli-tool version: [blue]{__version__}")
        raise typer.Exit()

def check_updates(value: bool):
    github = Github()
    repo = github.get_repo("andonihq/cli-tool")
    latest_version = repo.get_tags()[0].name
    current_version = __version__

    if latest_version != current_version:
        print(f"[bold][yellow] There is a new version available")

@app.command()
def get_secret(secret_name: str):
    try:
        client_sm = boto3.client('secretsmanager')
        secret = json.loads(client_sm.get_secret_value(SecretId=secret_name)['SecretString'])

        text = Text(justify="center")
        for key in secret:
            text.append(f"\n{key}", style="bold cyan")
            text.append(f": ", style="bold")
            text.append(f"{secret[key]}", style="italic")
        
        print(Panel.fit(text, title=f"[bold]AWS Secret - {secret_name}", border_style="gold3"))
    
    except Exception as e:
        typer.echo(f"Error: {e}")

@app.callback()
def main(
    version: bool = typer.Option(None, "-v", "--version", callback=version_callback, is_eager=True, help="Show version information."),
):
    return
   
if __name__ == "__main__":
    check_updates()
    app()