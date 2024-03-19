from pathlib import Path
from dataclasses import dataclass
import subprocess
import os

class GitCommandException(subprocess.CalledProcessError):
    pass

@dataclass
class GitRepo:
    name: str
    path: Path
    remote: str = None

    def __post_init__(self):
        self.path = Path(self.path) if self.path is not None else None
        if self.remote is None:
            self.remote = self.get_remote(self.path)
    
    @staticmethod
    def is_repo(path:str) -> bool:
        repodir =  Path(path)
        if repodir.exists():
            gitdir = repodir / '.git'
            return gitdir.is_dir()
        raise FileNotFoundError(f'is_repo: {repodir} does not exist')

    @staticmethod
    def get_remote(path:str) -> str:
        cwd = os.getcwd()
        os.chdir(Path(path).resolve())
        command = 'git remote -v'.split()
        try:
            result = subprocess.run(command, check=True, shell=False, capture_output=True, text=True)
            if result.stdout:
                name, url, mode = result.stdout.split('\n')[0].split()
                return url
            else:
                return None
        except subprocess.CalledProcessError as cpe:
            raise GitCommandException(**vars(cpe))
        finally:
            os.chdir(cwd)

