print(f'IMPORT | {__name__}')

from pathlib import Path
import re

from modules.simplegit.repo import GitRepo
from modules.simplegit.status import GitStatus

# print('from . import git_command')
from . import git_command
# print('from .git_command import GitCommandException')
from .git_command import GitCommandException

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

def get_status(repo:GitRepo) -> GitStatus:
    '''
    git status --branch --porcelain
    ## master...origin/master [ahead 4]
    M modules/git_helper.py
    '''
    command = 'git status --branch --porcelain'
    result = git_command.run(command, repo.path)

    branchstatus, *lines =  result.stdout.split('\n')
    branch_pattern = r'^## ([^ .]+)(\.{3}(\S+))*( \[{0,1}(\S+) (\d+)\]{0,1})*$'
    res = re.match(branch_pattern, branchstatus).groups()
    # print(f'{res = }')
    branch, _, remote, _, position, commits = res
    if position == 'ahead':
        push = True
        pull = False
    elif position == 'behind':
        push = False
        pull = True
    else:
        push = False
        pull = False
    
    added = []
    modified = []
    deleted = []
    untracked = []
    dirty = False
    for line in lines:
        if len(line):
            index = line[0]
            workspace = line[1]
            filename = line[2:]
            dirty = True
            match workspace:
                case 'A':
                    added.append(filename)
                case 'M':
                    modified.append(filename)
                case 'D':
                    deleted.append(filename)
                case '?':
                    untracked.append(filename)
    
    status = GitStatus(branch, remote, position, commits,
                       modified, added, deleted, untracked, 
                       dirty, push, pull)
    return status
