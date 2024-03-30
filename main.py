import json
from vscode import Workspace
from atrox3d.simplegit import git

if __name__ == '__main__':
    ws = Workspace('code-workspace.code-workspace')
    for repo in ws.get_repos(recurse=False):
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

    print(json.dumps(list(ws.get_clones()), indent=2))
