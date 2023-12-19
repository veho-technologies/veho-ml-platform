from typing import List

from anyscale.sdk.anyscale_client.models import CreateProject, ProjectsQuery, ProjectResponse

from veho_ml.schemas import VehoProjects
from veho_ml.utils import sdk


def list_projects() -> VehoProjects:
    # TODO: This should also fetch the Optional Repository associated with each project
    
    res = sdk.search_projects(ProjectsQuery())
    return VehoProjects(projects={project.name: {"id": project.id} for project in res.results})

def get_project_id_by_name(project_name: str):
    project = list_projects().projects.get(project_name)
    if project:
        return project.id
    return None

def add_anyscale_project(name: str) -> ProjectResponse:
    return sdk.create_project(CreateProject(name=name))

def create_project(name: str, no_repo: bool = False) -> ProjectResponse:
    # TODO: Print more useful output
    return add_anyscale_project(name)

