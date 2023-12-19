from typing import Dict

from pydantic import BaseModel

class VehoProject(BaseModel):
    id: str

class VehoProjects(BaseModel):
    projects: Dict[str, VehoProject]

class VehoWorkspace(BaseModel):
    id: str
    state: str
    url: str

class VehoWorkspaces(BaseModel):
    workspaces: Dict[str, VehoWorkspace]