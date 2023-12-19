from typing import List

from rich.console import Console
from rich.table import Table
import typer

from veho_ml.projects import list_projects
from veho_ml.schemas import VehoProjects, VehoWorkspaces
from veho_ml.utils import sdk
from veho_ml.workspaces import list_workspaces


app = typer.Typer()
console = Console()


@app.command()
def projects():
    projects = list_projects()

    table = Table("Project-Name", "id")
    for name, project in projects.projects.items():
        table.add_row(name, project.id)

    console.print(table)


@app.command()
def workspaces():
    workspaces = list_workspaces()

    table = Table("Workspace-Name", "state", "url")
    for name, workspace in workspaces.workspaces.items():
        table.add_row(name, workspace.state, workspace.url)

    console.print(table)
