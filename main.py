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
            print(
                  f'{repo.name:30.30} '
                  f'{repo.get_path().stem:30.30} '
                  f'{status.position} '
                  f'{status.commits} '
                  f'{status.push} '
                  f'{status.pull} '
                  f'{"DIRTY" if status.dirty else ""}'
                  )
        except git.GitCommandException as gce:
            print(gce)
            exit()
    
    # test = git.get_repo('vscode', '.')
    # print(test)
    # status = git.get_status(test)
    # print(status)

    # print(json.dumps(list(ws.get_clones()), indent=2))
    # ws.save_clones('clones.json')
