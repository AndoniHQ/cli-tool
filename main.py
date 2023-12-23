import typer
import boto3
import json
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer()

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
   
if __name__ == "__main__":
    app()