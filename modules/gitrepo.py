from pathlib import Path
from dataclasses import dataclass
# import subprocess
# import os

from . import git_helper as git
# class GitCommandException(subprocess.CalledProcessError):
    # pass

@dataclass
class GitRepo:
    name: str
    path: Path
    remote: str = None

    # def __post_init__(self):
        # self.path = Path(self.path) if self.path is not None else None
        # if self.remote is None:
            # self.remote = git.get_remote(self.path)
