"""Adds full features CLI functionality to the gpull module."""
import typer

from .gpull import gpull


app = typer.Typer()
app.command()(gpull)


if __name__ == "__main__":
    app()
