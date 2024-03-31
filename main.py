import json
from pathlib import Path
from vscode_workspace import VsCodeWorkspace
from atrox3d.simplegit import git

def get_gitrepos(ws:VsCodeWorkspace, absolute=False, recurse=False):
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
                yield git.get_repo(name, repo_git_folder.parent)
        else:
            try:
                yield git.get_repo(name, path)
            except git.NotAGitRepo:
                pass


if __name__ == '__main__':
    ws = VsCodeWorkspace('code-workspace.code-workspace')
    for repo in get_gitrepos(ws, recurse=True):
        try:
            status = git.get_status(repo)
            action = f'PUSH({status.commits})' if status.push else f'PULL({status.commits})' if status.pull else 'NO_ACTION'
            dirty = f'DIRTY({len(status.added)+len(status.deleted)+len(status.modified)+len(status.untracked)})' if status.dirty else ""
            print(
                  f'{repo.name:30.30} '
                  f'{repo.get_path().stem:30.30} '
                  f'{action:{len("NO_ACTION")}.{len("NO_ACTION")}} '
                  f'{dirty}'
                  )
        except git.GitCommandException as gce:
            print(gce)
            exit()
