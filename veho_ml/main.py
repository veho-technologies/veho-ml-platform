import typer

from veho_ml import projects, workspaces
from veho_ml.commands import create, list


app = typer.Typer()
app.add_typer(create.app, name="create")
app.add_typer(list.app, name="list")
