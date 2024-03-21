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

@dataclass
class GitStatus:
    '''
    4.2. Status Flags
    Furthermore, the status flag consists of two characters. 
    If we're not performing a merge operation, 
    the first character shows the index status 
    while the second shows the workspace status.

    The above example shows four different status flags:

     M: modified
     A: Added
     D: deleted
    ??: unknown to the index
    
    Additionally, the -porcelain option accepts a version property with two 
    available values, 1 and 2. 
    If we don't set a value, version 1 is the default. 
    Also, version 1 is guaranteed not to change in the future 
    and is more concise than version 2. 
    As a result, it's easier and safer to use it within a script.
    '''
    branch: str
    remote: str
    position: str
    count:str
    modified: list
    added: list
    deleted: list
    untracked: list
    dirty: bool
    push: bool
    pull: bool

import re
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
    branch, _, remote, _, position, count = res
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
    status = GitStatus(
                    branch, remote, position, count, modified, 
                    added, deleted, untracked, dirty, 
                    push, pull
                    )
    return status
