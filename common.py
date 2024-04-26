from pathlib import Path
from typing import Generator

from vscode_workspace import VsCodeWorkspace
from atrox3d.simplegit import git


def get_gitrepos(ws:VsCodeWorkspace, absolute=False, recurse=False) -> Generator[git.GitRepo, None, None]:
    '''
    return a list of GitRepo objects for each workspace folder,
    excluding non-git repos

    if recurse==True, searches recursively every git repo inside 
    each workspace item

    if absolute==True, the paths are converted to absolute paths
    '''
    for name, path in ws.get_configtuples():
        path = Path(path).resolve() if absolute else Path(path)
        if recurse:
            for repo_git_folder in path.glob('**/.git/'):
                yield git.get_repo(repo_git_folder.parent, name=name)
        else:
            try:
                yield git.get_repo(path, name=name)
            except git.GitNotARepoException:
                pass