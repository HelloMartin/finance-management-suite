import typer

app = typer.Typer()


@app.callback()
def callback() -> None:
    """Finance Management Suite CLI."""


@app.command()
def hello() -> None:
    """Small command to verify the CLI works."""
    typer.echo("Finance Management Suite")


def main() -> None:
    app()
