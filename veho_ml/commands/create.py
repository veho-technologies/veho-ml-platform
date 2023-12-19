from anyscale.sdk.anyscale_client.models import CreateProject, ProjectsQuery, ProjectResponse
from rich import print
import typer

from veho_ml.config import config
from veho_ml.projects import create_project, get_project_id_by_name, list_projects
from veho_ml.workspaces import create_anyscale_workspace

app = typer.Typer()


@app.command()
def project(
    name: str,
    no_repo: bool = typer.Option(
        False, "--no-repo", help="If set, no repository will be created."
    ),
    no_workspace: bool = typer.Option(
        False, "--no-workspace", help="If set, no workspace will be created."
    )):
    if name in list_projects():
        # TODO: Print associated repo also if applicable
        raise typer.BadParameter(f"The project name '{name}' already exists.")
    print(f"Creating project [bold blue]name[/bold blue]" + (f" under repository [bold blue]xxxxx[/bold blue]" * (no_repo is False)))
    create_project(name, no_repo)

@app.command()
def workspace(
    name: str,
    project_name: str = typer.Option(
        None, "--project-name", help="Workspace will be built for this project, Sandbox by default."
    )):
    if not project_name:
        print(f"[bold red]Warning: [/bold red] project-name not set, using default project [bold blue]{config.default_project_name}[/bold blue]")
        project_name = config.default_project_name
    project_id = get_project_id_by_name(project_name)
    if not project_id:
        raise typer.BadParameter(f"The project name '{project_name}' does not exist.")
    print(f"Creating workspace [bold blue]{name}[/bold blue] under [bold blue]{project_name}[/bold blue] project")
    create_anyscale_workspace(name, project_id)
