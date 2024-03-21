from pathlib import Path
import os

from .gitrepo import GitRepo
from . import git_command

class NotAGitRepo(Exception):
    pass

def get_repo(name: str, path:str) -> GitRepo:
    if is_repo(path):
        remote = get_remote(path)
        repo = GitRepo(name, path, remote)
        return repo
    raise NotAGitRepo(f'path {path} is not a git repo')

def is_repo(path:str) -> bool:
    repodir =  Path(path)
    if repodir.exists():
        gitdir = repodir / '.git'
        return gitdir.is_dir()
    raise FileNotFoundError(f'is_repo: {repodir} does not exist')

@git_command.pushd
def get_remote(path:str) -> str:
    os.chdir(Path(path).resolve())
    result = git_command.run('git remote -v')
    if result.stdout:
        name, url, mode = result.stdout.split('\n')[0].split()
        return url
    else:
        return None
