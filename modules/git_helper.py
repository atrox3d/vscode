from pathlib import Path

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

def get_remote(path:str) -> str:
    result = git_command.run('git remote -v', path)
    if result.stdout:
        name, url, mode = result.stdout.split('\n')[0].split()
        return url
    else:
        return None

def status(path:str):
    '''
    git status --branch --porcelain
    ## master...origin/master [ahead 4]
    M modules/git_helper.py
    '''
    result = git_command.run('git status --branch --porcelain', path)
    if result.stdout:
        for line in result.stdout.split('\n'):
            print(line)
    else:
        return None
