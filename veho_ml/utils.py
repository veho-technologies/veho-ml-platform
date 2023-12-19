from rich import print
import subprocess
import sys
from typing import List

from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models import ProjectsQuery

sdk = AnyscaleSDK()


def list_project_names() -> List[str]:
    # TODO: This should also fetch the Optional Repository associated with each project
    return [project.name for project in sdk.search_projects(ProjectsQuery()).results]

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[bold red]An error occurred: {e.stderr}[/bold red]")
        sys.exit()
