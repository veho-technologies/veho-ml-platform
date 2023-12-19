from pydantic import BaseModel

class Config(BaseModel):
    default_cloud_id: str = "cld_2nsihlbm1xztiftrwjup4iyiy9"
    default_cluster_env_build_id: str = "anyscaleray280-py38"
    default_compute_config_id: str = "cpt_94i5t66uzrapvvpkn7liagjlwi"
    default_project_name: str = "veho-sandbox"

config = Config()
