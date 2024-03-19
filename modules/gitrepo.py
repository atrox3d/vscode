from pathlib import Path
from dataclasses import dataclass
from . import git_helper as git

@dataclass
class GitRepo:
    name: str
    path: Path
    remote: str

    def __post_init__(self):
        self.path = Path(self.path) if self.path is not None else None

