from pathlib import Path
import subprocess
import os

from .gitrepo import GitRepo
from . import git_command

class GitCommandException(subprocess.CalledProcessError):
    pass

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
    # cwd = os.getcwd()
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
    # finally:
        # os.chdir(cwd)

if __name__ == '__main__':
    import sys
    path = Path(sys.argv[1]).resolve()
    
    if is_repo(path):
        try:
            print(get_remote(path))
        except GitCommandException as gce:
            print(gce.stderr)
    else:
        print(f'not a git repo: {path}')
