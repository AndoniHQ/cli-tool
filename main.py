import typer
import boto3
import json
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

def update_callback(value: bool):
    if value:
        update()
        raise typer.Exit()

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
    update: bool = typer.Option(None, "-u", "--update", callback=update_callback, is_eager=True, help="Update cli-tool"),
):
    return
   
if __name__ == "__main__":
    app()