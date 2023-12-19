from rich import print
import time
from typing import List, Optional

from anyscale.sdk.anyscale_client.models import CreateProject, ProjectsQuery, ProjectResponse

from veho_ml.config import config
from veho_ml.utils import run_command, sdk, list_project_names
from veho_ml.projects import get_project_id_by_name
from veho_ml.schemas import VehoWorkspaces

def create_anyscale_workspace(
        workspace_name: str,
        project_id: str,
        cloud_id: Optional[str] = None,
        cluster_env_build_id: Optional[str] = None,
        compute_config_id: Optional[str] = None
    ):
        result = run_command([
            "anyscale", "workspace", "create", 
            "--name", workspace_name,
             "--project-id", project_id,
             "--cloud-id", cloud_id or config.default_cloud_id,
             "--cluster-env-build-id", cluster_env_build_id or config.default_cluster_env_build_id,
             "--compute-config-id", compute_config_id or config.default_compute_config_id
        ])
        print("[bold green]Workspace cluster starting...[/bold green]")
        poll_workspace_for_status(workspace_name)

def poll_workspace_for_status(workspace_name: str):
    # Step 2: Poll for workspace status
    timeout = 600  # 10 minutes in seconds
    poll_interval = 10  # Check every 10 seconds
    start_time = time.time()
    while time.time() - start_time < timeout:
        workspaces = list_workspaces()
        workspace = workspaces.workspaces.get(workspace_name)
        status = workspace.state if workspace else None
        
        if status == "Running":
            print("[bold green]Workspace is up and running.[/bold green]")
            return
        elif status == "StartingUp":
            print("[bold yellow]Workspace is StartingUp...[/bold yellow]")  
        elif status is not None and status != "StartingUp":
            print("[bold red]Workspace is in unhealthy state, please check the logs.[/bold red]")
            return

        time.sleep(poll_interval)

    print("[bold red]Timeout reached while waiting for the workspace to start.[/bold red]")

def list_workspaces() -> VehoWorkspaces:
    output = run_command(["anyscale", "workspace", "list"])
    # Split the output into lines
    lines = output.strip().split('\n')
    # Parse each line
    workspaces = {}
    for line in lines[2:]:  # Skip the header lines
        parts = line.split()
        if len(parts) < 4:
            continue  # Skip malformed lines

        # Extracting details (assuming fixed column order)
        name, id, state, url = parts[0], parts[1], parts[2], parts[3]
        workspaces[name] = {'id': id, 'state': state, 'url': url}
    return VehoWorkspaces(workspaces=workspaces)
