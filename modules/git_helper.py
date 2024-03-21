from pathlib import Path
from dataclasses import dataclass

from . import git_command
from .git_command import GitCommandException

@dataclass
class GitRepo:
    name: str
    path: Path
    remote: str = None

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

def status(repo:GitRepo):
    '''
    git status --branch --porcelain
    ## master...origin/master [ahead 4]
    M modules/git_helper.py
    '''
    command = 'git status --branchx --porcelain'
    result = git_command.run(command, repo.path)
    if result.stdout:
        for line in result.stdout.split('\n'):
            print(line)
    if result.stderr:
        for line in result.stderr.split('\n'):
            print(line)
    else:
        return None
