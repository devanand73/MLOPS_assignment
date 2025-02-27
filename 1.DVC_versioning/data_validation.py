# data_validation.py
from dvc.repo import Repo

def get_data_lineage():
    repo = Repo()
    return repo.ls(
        targets=["data/processed.dvc"],
        revs=["HEAD"],
        recursive=True,
        all_tags=True
    )